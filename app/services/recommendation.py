from sqlalchemy.orm import Session
from app.crud.recommendation import get_user_interactions
from app.crud.product import get_products_by_ids
from app.models.product import ProductModel
from app.models.recommendation import UserInteractionModel
from app.models.vendor import VendorModel

def recommend_products(user_id: int, db: Session):
    # Fetch user interaction data
    user_data = db.query(UserInteractionModel).filter(UserInteractionModel.user_id == user_id).all()

    # Implement a basic recommendation algorithm (e.g., collaborative filtering)
    # For demonstration purposes, let's return random products
    recommended_product_ids = [interaction.product_id for interaction in user_data]

    # Fetch recommended products from the database
    recommended_products = db.query(ProductModel).filter(ProductModel.id.in_(recommended_product_ids)).all()
    return recommended_products

def recommend_products_user_based(user_id: int, db: Session):
    # Fetch user interaction data
    user_data = db.query(UserInteractionModel).filter(UserInteractionModel.user_id == user_id).all()

    # Find similar users based on interaction patterns
    similar_users = db.query(UserInteractionModel.user_id).filter(UserInteractionModel.product_id.in_(
        [interaction.product_id for interaction in user_data])).distinct()

    # Recommend products that these similar users have interacted with
    recommended_product_ids = db.query(UserInteractionModel.product_id).filter(
        UserInteractionModel.user_id.in_(similar_users)).distinct()

    recommended_products = db.query(ProductModel).filter(
        ProductModel.id.in_(recommended_product_ids)).all()

    return recommended_products

def recommend_products_item_based(user_id: int, db: Session):
    # Fetch user interaction data
    user_data = db.query(UserInteractionModel).filter(UserInteractionModel.user_id == user_id).all()

    # Find products that similar users have interacted with
    similar_product_ids = db.query(UserInteractionModel.product_id).filter(UserInteractionModel.user_id.in_(
        db.query(UserInteractionModel.user_id).filter(UserInteractionModel.product_id.in_(
            [interaction.product_id for interaction in user_data])).distinct())).distinct()

    recommended_products = db.query(ProductModel).filter(
        ProductModel.id.in_(similar_product_ids)).all()

    return recommended_products

def recommend_products_content_based(user_id: int, db: Session):
    # Fetch user interaction data
    user_data = db.query(UserInteractionModel).filter(UserInteractionModel.user_id == user_id).all()

    # Gather features of the interacted products
    interacted_products = db.query(ProductModel).filter(
        ProductModel.id.in_([interaction.product_id for interaction in user_data])).all()

    # For demonstration, let's match products by the same category and price range
    category = interacted_products[0].description
    price = interacted_products[0].price

    recommended_products = db.query(ProductModel).filter(
        ProductModel.description == category,
        ProductModel.price.between(price * 0.8, price * 1.2)
    ).all()

    return recommended_products

def recommend_products_hybrid(user_id: int, db: Session):
    user_based_recommendations = recommend_products_user_based(user_id, db)
    content_based_recommendations = recommend_products_content_based(user_id, db)

    # Combine both lists, ensuring no duplicates
    combined_recommendations = {product.id: product for product in user_based_recommendations + content_based_recommendations}.values()

    return list(combined_recommendations)

def recommend_vendors(user_id: int, db: Session):
    # Fetch user interaction data
    user_data = db.query(UserInteractionModel).filter(UserInteractionModel.user_id == user_id).all()

    # Recommend vendors based on the user's product interactions
    recommended_vendor_ids = db.query(ProductModel.vendor_id).filter(
        ProductModel.id.in_([interaction.product_id for interaction in user_data])).distinct()

    recommended_vendors = db.query(VendorModel).filter(
        VendorModel.id.in_(recommended_vendor_ids)).all()

    return recommended_vendors