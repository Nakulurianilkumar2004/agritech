# app/modules/crop_recommendation/schemas.py
from pydantic import BaseModel


class CropRecommendationRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


class CropRecommendationResponse(BaseModel):
    predicted_crop: str