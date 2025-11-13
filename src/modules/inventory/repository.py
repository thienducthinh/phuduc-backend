from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.inventory.models import InventoryItem

class InventoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> InventoryItem:
        item = InventoryItem(**data)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def get_by_id(self, item_id: int) -> InventoryItem | None:
        query = select(InventoryItem).where(InventoryItem.id == item_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()