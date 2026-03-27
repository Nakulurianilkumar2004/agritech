from bson import ObjectId
from app.core.database import get_database


def create_crop_request(data: dict):
    db = get_database()
    return db.crop_requests.insert_one(data)


def get_all_requests():
    db = get_database()
    return list(db.crop_requests.find())


def get_user_requests(user_id: str):
    db = get_database()
    return list(db.crop_requests.find({"user_id": user_id}))


def update_request_status(request_id: str, status: str):
    db = get_database()
    return db.crop_requests.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": status}}
    )