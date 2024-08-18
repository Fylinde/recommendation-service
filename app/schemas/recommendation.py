from pydantic import BaseModel
from typing import List, Optional
from app.schemas.product import ProductSchema


class UserInteractionSchema(BaseModel):
    user_id: int
    product_id: int
    interaction_type: str
    interaction_value: float


class RecommendationResponseSchema(BaseModel):
    recommendations: List[ProductSchema]
    
    class Config:
        from_attributes = True