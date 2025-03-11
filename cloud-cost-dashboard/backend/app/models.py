# models.py
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AzureCostData(Base):
    __tablename__ = 'azure_cost_data'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)  # Date of the cost data
    service_name = Column(String)  # Name of the Azure service
    cost = Column(Float)  # Cost in USD
    currency = Column(String)  # Currency (e.g., USD)