from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from bson.binary import Binary

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["resume_analyzer_db"]

users_collection = db["users"]
jobs_collection = db["jobs"]

# Create a new user with hashed password (stored as Binary)
def create_user(email, password):
    from .user_model import get_user_by_email
    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and store as binary (no Base64 encoding)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    password_hash_binary = Binary(password_hash)  # Store as binary data

    try:
        result = users_collection.insert_one({
            "email": email,
            "password": password_hash_binary,
            "resumes": []
        })
        return {"user_id": str(result.inserted_id), "message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

# Get user by email
def get_user_by_email(email):
    try:
        return users_collection.find_one({"email": email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

# Verify if a given password matches the stored password hash
def verify_password(stored_hash_binary, password):
    try:
        # Use the stored binary hash directly (no Base64 decoding needed)
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash_binary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying password: {str(e)}")
