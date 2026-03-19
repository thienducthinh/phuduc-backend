from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date


DeliveryStatus = Literal["Pending", "In Transit", "Delivered", "Failed"]


class CarrierCreate(BaseModel):
    carrier_name: str
    carrier_phone: Optional[str] = None
    carrier_email: Optional[str] = None


class CarrierUpdate(BaseModel):
    carrier_name: Optional[str] = None
    carrier_phone: Optional[str] = None
    carrier_email: Optional[str] = None


class CarrierResponse(BaseModel):
    carrier_id: int
    carrier_name: str
    carrier_phone: Optional[str]
    carrier_email: Optional[str]

    class Config:
        from_attributes = True


class DeliveryCreate(BaseModel):
    sales_order_id: int
    carrier_id: Optional[int] = None
    delivery_address: str
    scheduled_date: date
    tracking_number: Optional[str] = None


class DeliveryUpdate(BaseModel):
    carrier_id: Optional[int] = None
    delivery_address: Optional[str] = None
    scheduled_date: Optional[date] = None
    delivered_date: Optional[date] = None
    status: Optional[DeliveryStatus] = None
    tracking_number: Optional[str] = None


class DeliveryResponse(BaseModel):
    delivery_id: int
    sales_order_id: int
    carrier_id: Optional[int]
    delivery_address: str
    scheduled_date: date
    delivered_date: Optional[date]
    status: str
    tracking_number: Optional[str]

    class Config:
        from_attributes = True
