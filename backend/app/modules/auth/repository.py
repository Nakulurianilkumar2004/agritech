from bson import ObjectId
from app.core.database import get_database


def get_user_by_email(email: str):
    db = get_database()
    return db.users.find_one({"email": email})


def get_user_by_id(user_id: str):
    db = get_database()
    return db.users.find_one({"_id": ObjectId(user_id)})


def create_user(user_data: dict):
    db = get_database()
    return db.users.insert_one(user_data)


def update_user_role(user_id: str, role: str):
    db = get_database()
    return db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": role}}
    )