from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date
from decimal import Decimal


PriceType = Literal["Customer 1", "Customer 2", "Customer 3"]


class PriceBookCreate(BaseModel):
    item_id: int
    price_type: PriceType
    price: Decimal
    effective_date: date
    expiry_date: Optional[date] = None
    is_active: bool = True


class PriceBookUpdate(BaseModel):
    price: Optional[Decimal] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None
    is_active: Optional[bool] = None


class PriceBookResponse(BaseModel):
    price_book_id: int
    item_id: int
    price_type: str
    price: Decimal
    effective_date: date
    expiry_date: Optional[date]
    is_active: bool

    class Config:
        from_attributes = True
