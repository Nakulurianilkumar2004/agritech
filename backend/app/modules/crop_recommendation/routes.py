# app/modules/crop_recommendation/routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.modules.crop_recommendation.schemas import CropRecommendationRequest, CropRecommendationResponse
from app.modules.crop_recommendation.service import predict_crop, load_crop_model
from app.core.dependencies import require_role, get_current_user

router = APIRouter()

# Load model at startup
load_crop_model()

@router.post("/predict", response_model=CropRecommendationResponse, summary="Predict crop")
def crop_recommendation(
    request: CropRecommendationRequest,
    user=Depends(require_role("user"))  # Only farmers can access
):
    """
    Predict the most suitable crop based on soil and weather features.
    """
    try:
        predicted = predict_crop(request.dict())
        return {"predicted_crop": predicted}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))