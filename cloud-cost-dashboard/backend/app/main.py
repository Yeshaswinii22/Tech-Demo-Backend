from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import crud, models
from app.get_azure_token import get_access_token, fetch_cost_data  # Import the functions

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/fetch-and-load-cost-data/")
def fetch_and_load_cost_data(db: Session = Depends(get_db)):
    """
    API Endpoint to fetch Azure cost data, transform it, and load into the database.
    """
    access_token = get_access_token()  #  Fetch the access token first
    cost_data = fetch_cost_data(access_token)  # Pass access_token to fetch_cost_data()
    return crud.transform_and_load_azure_cost_data(db, cost_data)
