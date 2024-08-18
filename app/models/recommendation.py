from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.database import BaseModel

class UserInteractionModel(BaseModel):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    interaction_type = Column(String, nullable=False)
    interaction_value = Column(Float, nullable=False)

    product = relationship("ProductModel", back_populates="interactions")

