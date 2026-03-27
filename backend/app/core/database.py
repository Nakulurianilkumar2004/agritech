from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.core.config import settings

client = MongoClient(
    settings.MONGO_URI,
    server_api=ServerApi("1")
)

database = client[settings.DATABASE_NAME]


def get_database():
    return database


def connect_to_mongo():
    try:
        client.admin.command("ping")
        print("✅ Connected to MongoDB Atlas")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)


def close_mongo_connection():
    client.close()
    print("🔴 MongoDB connection closed")