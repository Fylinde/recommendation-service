from sqlalchemy.orm import Session
from typing import List
from app.models.product import ProductModel

def get_products_by_ids(db: Session, product_ids: List[int]):
    return db.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()
