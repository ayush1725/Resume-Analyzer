# models/user_model.py
from pydantic import BaseModel
from bson.binary import Binary
from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["resume_analyzer_db"]

users_collection = db["users"]

# Utility function to hash password
def hash_password(password: str) -> Binary:
    try:
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return Binary(password_hash)  # Store as binary data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error hashing password: {str(e)}")

# Verify if a given password matches the stored password hash
def verify_password(stored_hash_binary: Binary, password: str) -> bool:
    try:
        # Use the stored binary hash directly (no Base64 decoding needed)
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash_binary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying password: {str(e)}")

# Create a new user with hashed password (stored as Binary)
def create_user(email: str, password: str):
    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and store as binary
    password_hash_binary = hash_password(password)

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
def get_user_by_email(email: str):
    try:
        return users_collection.find_one({"email": email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

