from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class SaleBase(BaseModel):
    product_id: str
    quantity: int
    total_price: float
    date: datetime

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: Optional[str] = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
