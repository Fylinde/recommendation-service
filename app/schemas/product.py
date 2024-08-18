from pydantic import BaseModel
from typing import List, Optional

class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    vendor_id: int

    class Config:
        from_attributes = True