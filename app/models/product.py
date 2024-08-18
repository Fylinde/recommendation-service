
from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.database import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    interactions = relationship("UserInteractionModel", back_populates="product")
    vendor = relationship("VendorModel", back_populates="products")
    