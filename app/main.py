from fastapi import FastAPI
import logging

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        # Your database initialization logic here
        # Example:
        # db = SessionLocal()
        # db.query(SomeModel).first()
        pass
    except Exception as e:
        logging.warning(f"Startup skipped: {e}")

@app.get("/")
def read_root():
    return {"message": "Recommendation service is running."}
