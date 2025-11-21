from pydantic import BaseModel
from typing import Optional


class POCreate(BaseModel):
    supplier_id: int


class POResponse(BaseModel):
    purchase_order_id: int
    supplier_id: Optional[int]

    class Config:
        from_attributes = True
