from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    quantity: int
    price: float

class ItemResponse(ItemCreate):
    id: int

    model_config = {"from_attributes": True}