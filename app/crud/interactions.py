from sqlalchemy.orm import Session
from app.models import UserInteractionModel, ProductModel

def get_user_ids(db: Session):
    """Fetch all unique user IDs from interactions."""
    return [interaction.user_id for interaction in db.query(UserInteractionModel.user_id).distinct()]

def get_item_ids(db: Session):
    """Fetch all product IDs."""
    return [product.id for product in db.query(ProductModel).all()]

def get_interactions(db: Session):
    """Fetch all user interactions as (user_id, product_id) tuples."""
    return [(interaction.user_id, interaction.product_id) for interaction in db.query(UserInteractionModel).all()]
