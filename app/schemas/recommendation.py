from pydantic import BaseModel
from typing import List, Dict, Optional
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
        
class StockingRecommendationSchema(BaseModel):
    product: ProductSchema
    warehouse_id: int
    recommended_quantity: Optional[int]  # Quantity recommended to be stocked at the warehouse

    class Config:
        from_attributes = True 
        
class DemandForecastSchema(BaseModel):
    product: ProductSchema
    demand_forecast: Dict[str, float]  # Mapping of date to predicted demand

    class Config:
        from_attributes = True               