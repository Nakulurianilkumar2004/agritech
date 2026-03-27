from fastapi import APIRouter, Depends
from app.modules.fertilizer.schemas import FertilizerInput
from app.modules.fertilizer.service import predict_fertilizer
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/fertilizer", tags=["fertilizer"])

# Example: Only logged-in users (role=user) or admin can predict
@router.post("/predict")
def predict(
    input: FertilizerInput,
    user=Depends(require_role("user"))  # Will also allow admin
):
    # `user` is the currently authenticated user dict
    return predict_fertilizer(input.dict())