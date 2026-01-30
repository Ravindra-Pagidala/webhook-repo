from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load .env (backup in case not loaded elsewhere)
load_dotenv()

mongo_client = None

def init_mongo(app):
    """Initialize MongoDB client once"""
    global mongo_client
    if mongo_client is None:
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise ValueError(" MONGODB_URI not set! Check .env file at project root.")
        mongo_client = MongoClient(uri)
        print(" MongoDB connected successfully!")
    else:
        print(" MongoDB already initialized")

def get_db():
    """Get events collection"""
    global mongo_client
    if mongo_client is None:
        raise RuntimeError("MongoDB not initialized")
    return mongo_client.github_webhooks.github_events
