
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCqREwfAsApRLrdgHSeA1q09pfVt0vOLPs",
    "authDomain": "legal-aid-ead1c.firebaseapp.com",
    "databaseURL": "https://legal-aid-ead1c-default-rtdb.firebaseio.com",
    "projectId": "legal-aid-ead1c",
    "storageBucket": "legal-aid-ead1c.firebasestorage.app",
    "messagingSenderId": "888124238174",
    "appId": "1:888124238174:web:5da2372465b7c1430ec7cf",
    "measurementId": "G-GEW1E0F7F1"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login():
    print("Login")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Login successful")
    except Exception as e:
        print(e)
    pass
def signup():
    print("Sign up")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print("Sign up successful")
    except Exception as e:
        print(e)
ans = input("Do you want to sign up or login? (s/l): ")
if ans == "s":
    signup()
elif ans == "l":
    login()
else:
    print("Invalid input")

