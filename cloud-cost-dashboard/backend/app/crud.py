import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from app.database import SessionLocal, engine
from app.models import AzureCostData  # Import models directly
from app.database import SessionLocal  # Correct import

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform_and_load_azure_cost_data(db: Session, cost_data: dict):
    """
    Transform Azure cost data using Pandas and load it into the database.
    """
    # Extract rows from the cost data
    rows = cost_data.get("properties", {}).get("rows", [])

    if not rows:
        logger.warning("No data found to process.")
        return {"message": "No data to process"}

    # Convert rows into a Pandas DataFrame
    df = pd.DataFrame(rows, columns=["cost", "usage_date", "service_name", "currency"])

    # Convert usage_date format (e.g., 20250301 → 2025-03-01)
    df["usage_date"] = pd.to_datetime(df["usage_date"].astype(str), format="%Y%m%d").dt.date

    # Drop duplicates and fill missing values if necessary
    df.drop_duplicates(inplace=True)
    df.fillna({"currency": "USD"}, inplace=True)

    # Log the transformed data
    logger.info(f"Transformed DataFrame:\n{df.head()}")

    # Convert DataFrame to a list of dictionaries for bulk insert
    data_to_insert = df.to_dict(orient="records")

    # Bulk insert into database
    db.bulk_insert_mappings(AzureCostData, data_to_insert)
    db.commit()

    logger.info("Cost data successfully transformed and loaded into the database.")
    return {"message": "Cost data processed and stored successfully"}





