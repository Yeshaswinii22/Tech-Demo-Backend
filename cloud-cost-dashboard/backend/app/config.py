import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://Yeshas:@localhost/cloud_costs")
    AZURE_TENANT_ID: str = os.getenv("AZURE_TENANT_ID")
    AZURE_CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET: str = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_SUBSCRIPTION_ID: str = os.getenv("AZURE_SUBSCRIPTION_ID")

settings = Settings()