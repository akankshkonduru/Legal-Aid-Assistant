from fastapi import FastAPI
from pydantic import BaseModel
import pyrebase

app = FastAPI()

firebaseConfig = {
    "apiKey": "AIzaSyCqREwfAsApRLrdgHSeA1q09pfVt0vOLPs",
    "authDomain": "legal-aid-ead1c.firebaseapp.com",
    "databaseURL": "https://legal-aid-ead1c-default-rtdb.firebaseio.com",
    "projectId": "legal-aid-ead1c",
    "storageBucket": "legal-aid-ead1c.appspot.com",   # FIXED
    "messagingSenderId": "888124238174",
    "appId": "1:888124238174:web:5da2372465b7c1430ec7cf",
    "measurementId": "G-GEW1E0F7F1"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class User(BaseModel):
    email: str
    password: str


@app.post("/signup")
def signup(user: User):
    try:
        auth.create_user_with_email_and_password(user.email, user.password)
        return {"message": "Signup successful"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/login")
def login(user: User):
    try:
        auth.sign_in_with_email_and_password(user.email, user.password)
        return {"message": "Login successful"}
    except Exception as e:
        return {"error": str(e)}
