import logging
from fastapi import FastAPI
from app.routes.recommendation import router as recommendation_router
from app.database import SessionLocal
from app.models.recommendation import UserInteractionModel

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI with metadata for Swagger
app = FastAPI(
    title="Recommendation Service API",
    description="API documentation for the Recommendation Service, which provides product recommendations based on user interactions.",
    version="1.0.0",
    openapi_tags=[
        {"name": "recommendations", "description": "Operations related to product recommendations"},
    ],
)

# Global variables to store the trained LightFM model and dataset
lightfm_model = None
lightfm_dataset = None

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    # Placeholder for model training logic, if needed in the future

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Recommendation Service"}

# Include the router
app.include_router(recommendation_router, prefix="/api/v1", tags=["recommendations"])
