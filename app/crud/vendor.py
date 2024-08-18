from sqlalchemy.orm import Session
from app.models.vendor import VendorModel
from typing import List

def get_vendors_by_ids(db: Session, vendor_ids: List[int]):
    return db.query(VendorModel).filter(VendorModel.id.in_(vendor_ids)).all()
