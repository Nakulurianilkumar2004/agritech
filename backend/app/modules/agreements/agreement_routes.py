from fastapi import APIRouter, Depends
from app.modules.agreements.agreement_schema import CropRequestSchema, UpdateStatusSchema
from app.modules.agreements.agreement_service import (
    submit_crop_request,
    get_my_requests,
    get_all_crop_requests,
    change_request_status
)
from app.core.dependencies import get_current_user

router = APIRouter()


# -------------------------
# FARMER: SUBMIT REQUEST
# -------------------------
@router.post("/request")
def create_request(data: CropRequestSchema, user=Depends(get_current_user)):
    return submit_crop_request(data, user)


# -------------------------
# FARMER: VIEW OWN REQUESTS
# -------------------------
@router.get("/my-requests")
def my_requests(user=Depends(get_current_user)):
    return get_my_requests(user)


# -------------------------
# ADMIN: VIEW ALL REQUESTS
# -------------------------
@router.get("/all")
def all_requests(user=Depends(get_current_user)):
    return get_all_crop_requests(user)


# -------------------------
# ADMIN: UPDATE STATUS
# -------------------------
@router.put("/update/{request_id}")
def update_status(request_id: str, data: UpdateStatusSchema, user=Depends(get_current_user)):
    return change_request_status(request_id, data.status, user)