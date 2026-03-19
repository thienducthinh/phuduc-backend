from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import PriceBook


class PriceBookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, price_book_id: int) -> PriceBook | None:
        result = await self.db.execute(
            select(PriceBook).where(PriceBook.price_book_id == price_book_id)
        )
        return result.scalar_one_or_none()

    async def get_by_item_and_price_type(self, item_id: int, price_type: str) -> PriceBook | None:
        result = await self.db.execute(
            select(PriceBook).where(
                PriceBook.item_id == item_id,
                PriceBook.price_type == price_type,
                PriceBook.is_active == True,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_item(self, item_id: int) -> list[PriceBook]:
        result = await self.db.execute(
            select(PriceBook).where(PriceBook.item_id == item_id)
        )
        return list(result.scalars().all())

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[PriceBook]:
        result = await self.db.execute(select(PriceBook).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: dict) -> PriceBook:
        entry = PriceBook(**data)
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def update(self, entry: PriceBook, data: dict) -> PriceBook:
        for field, value in data.items():
            setattr(entry, field, value)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def delete(self, entry: PriceBook) -> None:
        await self.db.delete(entry)
        await self.db.commit()
