from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    is_active: bool = Field(True, description="Whether item is active")


class ItemCreate(ItemBase):
    item_id: Optional[int] = Field(None, description="Item ID (must be 7 digits)")

    @field_validator("item_id")
    @classmethod
    def validate_item_id(cls, v):
        if v is not None and (v < 1000000 or v > 9999999):
            raise ValueError("item_id must be a 7-digit number (1000000-9999999)")
        return v


class ItemUpdate(BaseModel):
    item_id: Optional[int] = Field(None, description="Item ID (must be 7 digits)")
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("item_id")
    @classmethod
    def validate_item_id(cls, v):
        if v is not None and (v < 1000000 or v > 9999999):
            raise ValueError("item_id must be a 7-digit number (1000000-9999999)")
        return v


class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    page_size: int
