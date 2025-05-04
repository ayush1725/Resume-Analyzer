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
    # Initialize MongoDB client and select the database
    client = MongoClient(MONGO_URI)
    db = client["resume_analyzer_db"]  # Database name

    # Define collections
    users_collection = db["users"]
    jobs_collection = db["jobs"]

except ConnectionFailure as e:
    raise ConnectionError(f"Could not connect to MongoDB: {e}")
