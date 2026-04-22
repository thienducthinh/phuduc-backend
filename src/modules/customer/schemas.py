from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime


class CustomerBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    customer_address: Optional[str] = Field(None, max_length=255, description="Customer address")
    customer_phone: Optional[str] = Field(None, max_length=15, description="Customer phone number")
    customer_email: Optional[str] = Field(None, max_length=100, description="Customer email")
    price_type: Literal["Customer 1", "Customer 2", "Customer 3"] = Field(..., description="Customer price type")


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=255)
    customer_address: Optional[str] = Field(None, max_length=255)
    customer_phone: Optional[str] = Field(None, max_length=15)
    customer_email: Optional[str] = Field(None, max_length=100)
    price_type: Optional[Literal["Customer 1", "Customer 2", "Customer 3"]] = None

    @field_validator("customer_email")
    @classmethod
    def validate_email(cls, v):
        if v is not None and v != "" and "@" not in v:
            raise ValueError("Invalid email format")
        return v


class CustomerResponse(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True


class CustomerListResponse(BaseModel):
    customers: list[CustomerResponse]
    total: int
    page: int
    page_size: int
