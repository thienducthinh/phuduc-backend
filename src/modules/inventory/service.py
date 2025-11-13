from src.core.exceptions import ValidationError
from src.modules.inventory.repository import InventoryRepository
from src.modules.inventory.schemas import ItemCreate, ItemResponse
from sqlalchemy.ext.asyncio import AsyncSession

class InventoryService:
    def __init__(self, db: AsyncSession):
        self.repo = InventoryRepository(db)

    async def create_item(self, item: ItemCreate) -> ItemResponse:
        if item.quantity < 0:
            raise ValidationError("Quantity cannot be negative")
        if item.price < 0:
            raise ValidationError("Price cannot be negative")
        db_item = await self.repo.create(item.model_dump())
        return ItemResponse.from_orm(db_item)

    async def get_item(self, item_id: int) -> ItemResponse | None:
        db_item = await self.repo.get_by_id(item_id)
        return ItemResponse.from_orm(db_item) if db_item else None