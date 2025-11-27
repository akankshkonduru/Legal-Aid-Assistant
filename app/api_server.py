from fastapi import FastAPI, UploadFile, File, HTTPException
import pyrebase
import json
from pydantic import BaseModel
import uvicorn

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your chains
from src.combined_chain import CombinedLegalChatbot     
from src.document_chain import DocumentGeneratorChain

app = FastAPI(title="Legal Aid Assistant API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chains
chat_chain = CombinedLegalChatbot()
doc_chain = DocumentGeneratorChain()

# ----------- MODELS -----------
class ChatRequest(BaseModel):
    user_query: str

class DocumentRequest(BaseModel):
    template_name: str
    user_inputs: dict
    user_query: str


# ----------- ENDPOINTS -----------

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    response = chat_chain.generate(request.user_query)
    return {"response": response}


# @app.post("/document/generate")
# def generate_document(request: DocumentRequest):
#     pdf_path, text = doc_chain.generate(
#         template_name=request.template_name,
#         user_inputs=request.user_inputs,
#         user_query=request.user_query
#     )

#     return {
#         "message": "Document generated successfully",
#         "pdf_path": pdf_path,
#         "content_preview": text[:500]
#     }


# @app.post("/voice/chat")
# async def voice_chat_endpoint(file: UploadFile = File(...)):
#     # Save file temporarily
#     temp_path = f"temp_{file.filename}"
#     with open(temp_path, "wb") as f:
#         f.write(await file.read())

#     text = transcribe_audio(temp_path)
#     response = chat_chain.run(text)

#     return {
#         "transcription": text,
#         "response": response
#     }


@app.get("/session/reset")
def reset_memory():
    chat_chain.memory.reset()
    return {"status": "Memory cleared"}


# ----------- AUTHENTICATION -----------

firebaseConfig = {
    "apiKey": "AIzaSyCqREwfAsApRLrdgHSeA1q09pfVt0vOLPs",
    "authDomain": "legal-aid-ead1c.firebaseapp.com",
    "databaseURL": "https://legal-aid-ead1c-default-rtdb.firebaseio.com",
    "projectId": "legal-aid-ead1c",
    "storageBucket": "legal-aid-ead1c.appspot.com",
    "messagingSenderId": "888124238174",
    "appId": "1:888124238174:web:5da2372465b7c1430ec7cf",
    "measurementId": "G-GEW1E0F7F1"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

USERS_FILE = "users.json"

def save_user_to_file(user_data):
    users = []
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
        except:
            pass
    
    # Check if user already exists and update, or append
    for i, u in enumerate(users):
        if u.get("email") == user_data["email"]:
            users[i] = user_data
            break
    else:
        users.append(user_data)
        
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def get_user_from_file(email):
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
                for user in users:
                    if user.get("email") == email:
                        return user
        except:
            pass
    return None

class User(BaseModel):
    email: str
    password: str

class SignupUser(User):
    firstName: str
    lastName: str

@app.post("/signup")
def signup(user: SignupUser):
    try:
        auth.create_user_with_email_and_password(user.email, user.password)
        # Save additional details to local file
        save_user_to_file(user.dict())
        return {"message": "Signup successful"}
    except Exception as e:
        error_message = str(e)
        try:
            if "{" in error_message:
                json_part = error_message[error_message.find("{"):]
                error_data = json.loads(json_part)
                if "error" in error_data and "message" in error_data["error"]:
                    error_message = error_data["error"]["message"]
        except:
            pass
        raise HTTPException(status_code=400, detail=error_message)


@app.post("/login")
def login(user: User):
    try:
        auth.sign_in_with_email_and_password(user.email, user.password)
        # Fetch user details
        user_data = get_user_from_file(user.email)
        response = {"message": "Login successful"}
        if user_data:
            response["firstName"] = user_data.get("firstName", "")
            response["lastName"] = user_data.get("lastName", "")
        else:
            # Fallback if not found in local file
            response["firstName"] = "User"
            response["lastName"] = ""
            
        return response
    except Exception as e:
        error_message = str(e)
        try:
            if "{" in error_message:
                json_part = error_message[error_message.find("{"):]
                error_data = json.loads(json_part)
                if "error" in error_data and "message" in error_data["error"]:
                    error_message = error_data["error"]["message"]
        except:
            pass
        raise HTTPException(status_code=400, detail=error_message)


if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000)
