from fastapi import HTTPException
from app.modules.agreements.agreement_repository import (
    create_crop_request,
    get_all_requests,
    get_user_requests,
    update_request_status
)


# -------------------------
# FARMER SUBMIT REQUEST
# -------------------------
def submit_crop_request(data, user):

    request_data = {
        "user_id": str(user["_id"]),
        "crop_name": data.crop_name,
        "price": data.price,
        "harvested_date": str(data.harvested_date),
        "location": data.location,
        "phone": data.phone,
        "status": "pending"
    }

    result = create_crop_request(request_data)

    return {
        "message": "Request submitted successfully",
        "request_id": str(result.inserted_id)
    }


# -------------------------
# FARMER VIEW OWN REQUESTS
# -------------------------
def get_my_requests(user):
    requests = get_user_requests(str(user["_id"]))

    for r in requests:
        r["_id"] = str(r["_id"])

    return requests


# -------------------------
# ADMIN VIEW ALL REQUESTS
# -------------------------
def get_all_crop_requests(user):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    requests = get_all_requests()

    for r in requests:
        r["_id"] = str(r["_id"])

    return requests


# -------------------------
# ADMIN UPDATE STATUS
# -------------------------
def change_request_status(request_id, status, user):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    update_request_status(request_id, status)

    return {
        "message": f"Request {status} successfully"
    }