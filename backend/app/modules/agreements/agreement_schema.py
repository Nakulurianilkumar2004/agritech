from pydantic import BaseModel, Field
from datetime import date


class CropRequestSchema(BaseModel):
    crop_name: str
    price: float
    harvested_date: date
    location: str
    phone: str = Field(min_length=10, max_length=10)


class UpdateStatusSchema(BaseModel):
    status: str  # approved / rejected