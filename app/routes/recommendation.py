from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.services.recommendation import (
    recommend_products,
    recommend_products_content_based,
    recommend_products_hybrid,
    recommend_products_item_based,
    recommend_products_user_based,
    recommend_sellers,
    recommend_stocking_locations,  # New stocking recommendation
    predict_demand  # New demand prediction
)
from app.schemas.product import ProductSchema
from app.schemas.seller import SellerSchema
from app.schemas.recommendation import RecommendationResponseSchema
from typing import List
import logging
from app.models.seller import SellerModel
from app.models.product import ProductModel
from app.models.recommendation import UserInteractionModel
from app.crud.product import get_products_by_ids
from app.crud.interactions import get_interactions, get_item_ids, get_user_ids
from app.services.tf_recommender import TFRecommender
from app.schemas.recommendation import StockingRecommendationSchema, DemandForecastSchema
router = APIRouter()

# Initialize the TFRS model globally
tf_recommender = None

logging.info("Defining routes for the recommendation service...")

@router.get("/recommendations/{user_id}", response_model=RecommendationResponseSchema)
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    recommendations = recommend_products(user_id, db)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return {"recommendations": [ProductSchema.from_orm(product) for product in recommendations]}

@router.get("/recommendations/collaborative/{user_id}", response_model=List[ProductSchema])
def get_recommendations_collaborative(user_id: int, db: Session = Depends(get_db)):
    recommendations = recommend_products_user_based(user_id, db)
    if not recommendations:
        logging.info(f"No collaborative recommendations found for user {user_id}.")
        raise HTTPException(status_code=404, detail="No recommendations found")
    
    logging.info(f"Found {len(recommendations)} collaborative recommendations for user {user_id}.")
    return [ProductSchema.from_orm(product) for product in recommendations]

@router.get("/recommendations/content/{user_id}", response_model=List[ProductSchema])
def get_recommendations_content(user_id: int, db: Session = Depends(get_db)):
    recommendations = recommend_products_content_based(user_id, db)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No content-based recommendations found")
    return [ProductSchema.from_orm(product) for product in recommendations]

@router.get("/recommendations/hybrid/{user_id}", response_model=List[ProductSchema])
def get_recommendations_hybrid(user_id: int, db: Session = Depends(get_db)):
    recommendations = recommend_products_hybrid(user_id, db)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No hybrid recommendations found")
    return [ProductSchema.from_orm(product) for product in recommendations]

@router.get("/seller-recommendations/{user_id}", response_model=List[SellerSchema])
def get_seller_recommendations(user_id: int, db: Session = Depends(get_db)):
    recommendations = recommend_sellers(user_id, db)
    
    if not recommendations:
        logging.info(f"No seller recommendations found for user {user_id}.")
        raise HTTPException(status_code=404, detail="No recommendations found")
    
    logging.info(f"Found {len(recommendations)} seller recommendations for user {user_id}.")
    return [SellerSchema.from_orm(seller) for seller in recommendations]

# New

# New endpoint for stocking recommendations
@router.get("/recommendations/stocking/{seller_id}", response_model=List[StockingRecommendationSchema])
def get_stocking_recommendations(seller_id: int, db: Session = Depends(get_db)):
    """
    API to provide stocking recommendations for sellers based on historical sales data and buyer locations.
    
    :param seller_id: The ID of the seller.
    :param db: The database session.
    :return: A list of recommended products with stocking suggestions.
    """
    recommendations = recommend_stocking_locations(seller_id, db)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No stocking recommendations found")
    return recommendations


# New endpoint for demand prediction
@router.get("/recommendations/demand/{seller_id}", response_model=List[DemandForecastSchema])
def get_demand_prediction(seller_id: int, db: Session = Depends(get_db)):
    """
    API to predict product demand for a seller based on historical sales data.
    
    :param seller_id: The ID of the seller.
    :param db: The database session.
    :return: A dictionary with demand predictions.
    """
    try:
        demand_forecast = predict_demand(seller_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting demand: {e}")
    
    return demand_forecast


# Initialize the TensorFlow recommender during the app startup event
@router.on_event("startup")
def initialize_tf_recommender():
    global tf_recommender

    logging.info("Initializing TensorFlow Recommender...")

    # Create a new database session
    db: Session = SessionLocal()

    try:
        # Fetch user_ids, item_ids, and interactions from the database
        user_ids = get_user_ids(db)
        item_ids = get_item_ids(db)
        interactions = get_interactions(db)

        if not user_ids or not item_ids or not interactions:
            raise ValueError("Insufficient data to train recommender model.")

        # Initialize and train the recommender
        tf_recommender = TFRecommender(user_ids=user_ids, item_ids=item_ids)
        tf_recommender.train(interactions=interactions)

        logging.info("TensorFlow Recommender initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize recommender: {e}")
        raise HTTPException(status_code=500, detail="Failed to initialize recommender")
    finally:
        # Close the database session
        db.close()

@router.get("/recommendations/tfrs/{user_id}")
def get_tf_recommendations(user_id: str, db: Session = Depends(get_db)):
    global tf_recommender

    if tf_recommender is None:
        raise HTTPException(status_code=500, detail="Model not initialized")

    try:
        recommendations = tf_recommender.recommend(user_id)
    except Exception as e:
        logging.error(f"Failed to get recommendations for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching recommendations")

    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")

    return {"user_id": user_id, "recommendations": recommendations}

# Route to create dummy data for testing purposes
@router.post("/create_dummy_data/")
def create_dummy_data(db: Session = Depends(get_db)):
    logging.info("Creating dummy data...")

    # Create dummy sellers
    seller1 = SellerModel(name="Tech Store", description="Your one-stop shop for tech gadgets", rating=4.5)
    seller2 = SellerModel(name="Gadget Hub", description="Latest and greatest in tech", rating=4.7)
    db.add_all([seller1, seller2])
    db.commit()
    db.refresh(seller1)
    db.refresh(seller2)

    # Create dummy products
    product1 = ProductModel(name="Smartphone X", description="Latest smartphone with amazing features", price=999.99, seller_id=seller1.id)
    product2 = ProductModel(name="Laptop Pro", description="High-performance laptop for professionals", price=1299.99, seller_id=seller2.id)
    product3 = ProductModel(name="Smartwatch Z", description="Smartwatch with health tracking features", price=199.99, seller_id=seller1.id)
    db.add_all([product1, product2, product3])
    db.commit()
    db.refresh(product1)
    db.refresh(product2)
    db.refresh(product3)

    # Create dummy user interactions
    interaction1 = UserInteractionModel(user_id=1, product_id=product1.id, interaction_type="view", interaction_value=1.0)
    interaction2 = UserInteractionModel(user_id=1, product_id=product2.id, interaction_type="purchase", interaction_value=1.0)
    interaction3 = UserInteractionModel(user_id=2, product_id=product3.id, interaction_type="view", interaction_value=1.0)
    db.add_all([interaction1, interaction2, interaction3])
    db.commit()

    logging.info("Dummy data created successfully.")
    return {"status": "success", "sellers": [seller1, seller2], "products": [product1, product2, product3], "interactions": [interaction1, interaction2, interaction3]}
