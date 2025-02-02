from sqlalchemy.orm import Session
from app.models.recommendation import UserInteractionModel

def get_user_interactions(db: Session, user_id: str):
    return db.query(UserInteractionModel).filter(UserInteractionModel.user_id == user_id).all()

