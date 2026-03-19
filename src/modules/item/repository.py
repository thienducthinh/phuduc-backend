from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Item, ItemBrand, ItemCategory


class ItemBrandRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, brand_id: int) -> ItemBrand | None:
        result = await self.db.execute(select(ItemBrand).where(ItemBrand.brand_id == brand_id))
        return result.scalar_one_or_none()

    async def get_by_code(self, brand_code: str) -> ItemBrand | None:
        result = await self.db.execute(select(ItemBrand).where(ItemBrand.brand_code == brand_code))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ItemBrand]:
        result = await self.db.execute(select(ItemBrand).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: dict) -> ItemBrand:
        brand = ItemBrand(**data)
        self.db.add(brand)
        await self.db.commit()
        await self.db.refresh(brand)
        return brand

    async def update(self, brand: ItemBrand, data: dict) -> ItemBrand:
        for field, value in data.items():
            setattr(brand, field, value)
        await self.db.commit()
        await self.db.refresh(brand)
        return brand

    async def delete(self, brand: ItemBrand) -> None:
        await self.db.delete(brand)
        await self.db.commit()


class ItemCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> ItemCategory | None:
        result = await self.db.execute(select(ItemCategory).where(ItemCategory.category_id == category_id))
        return result.scalar_one_or_none()

    async def get_by_code(self, category_code: str) -> ItemCategory | None:
        result = await self.db.execute(select(ItemCategory).where(ItemCategory.category_code == category_code))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ItemCategory]:
        result = await self.db.execute(select(ItemCategory).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: dict) -> ItemCategory:
        category = ItemCategory(**data)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update(self, category: ItemCategory, data: dict) -> ItemCategory:
        for field, value in data.items():
            setattr(category, field, value)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category: ItemCategory) -> None:
        await self.db.delete(category)
        await self.db.commit()


class ItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, item_id: int) -> Item | None:
        result = await self.db.execute(select(Item).where(Item.item_id == item_id))
        return result.scalar_one_or_none()

    async def get_by_code(self, item_code: str) -> Item | None:
        result = await self.db.execute(select(Item).where(Item.item_code == item_code))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[Item]:
        result = await self.db.execute(select(Item).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(Item))
        return result.scalar_one()

    async def search(self, query: str, skip: int = 0, limit: int = 10) -> list[Item]:
        result = await self.db.execute(
            select(Item)
            .where(Item.item_name.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, data: dict) -> Item:
        item = Item(**data)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item: Item, data: dict) -> Item:
        for field, value in data.items():
            setattr(item, field, value)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        await self.db.delete(item)
        await self.db.commit()
