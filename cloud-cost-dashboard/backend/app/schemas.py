from pydantic import BaseModel
from datetime import date

class AzureCostCreate(BaseModel):
    cost: float
    usage_date: date
    service_name: str
    currency: str

class AzureCostResponse(AzureCostCreate):
    id: int
    class Config:
        from_attributes = True  # This allows ORM support
