from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_db
from src.modules.inventory.dependencies import get_inventory_user
from src.modules.inventory.schemas import ItemCreate, ItemResponse
from src.modules.inventory.service import InventoryService

router = APIRouter()

@router.post("/items/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_inventory_user)
):
    service = InventoryService(db)
    try:
        return await service.create_item(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_inventory_user)
):
    service = InventoryService(db)
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item