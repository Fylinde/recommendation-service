from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseModel

class VendorModel(BaseModel):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    rating = Column(Float, nullable=True)

    products = relationship("ProductModel", back_populates="vendor")
