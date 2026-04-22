from sqlalchemy.ext.asyncio import AsyncSession

from .models import PriceBook
from .repository import PriceBookRepository
from .schemas import PriceBookCreate, PriceBookUpdate


class PriceBookService:
    def __init__(self, db: AsyncSession):
        self.repo = PriceBookRepository(db)

    async def get(self, price_book_id: int) -> PriceBook | None:
        return await self.repo.get_by_id(price_book_id)

    async def get_by_item(self, item_id: int) -> list[PriceBook]:
        return await self.repo.get_by_item(item_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[PriceBook]:
        return await self.repo.get_all(skip=skip, limit=limit)

    async def create(self, data: PriceBookCreate) -> PriceBook:
        return await self.repo.create(data.model_dump())

    async def update(self, entry: PriceBook, data: PriceBookUpdate) -> PriceBook:
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(entry, update_data)

    async def delete(self, entry: PriceBook) -> None:
        await self.repo.delete(entry)
