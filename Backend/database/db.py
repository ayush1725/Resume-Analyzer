from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

# Load MongoDB URI securely from environment variable
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file.")

try:
    client = MongoClient(MONGO_URI)
    db = client["resume_analyzer_db"]  # Database name
    users_collection = db["users"]
    jobs_collection = db["jobs"]
except ConnectionFailure as e:
    raise ConnectionError(f"Could not connect to MongoDB: {e}")
