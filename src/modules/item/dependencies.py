from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from .models import Item, ItemBrand, ItemCategory
from .repository import ItemRepository, ItemBrandRepository, ItemCategoryRepository


async def get_item_or_404(item_id: int, db: AsyncSession = Depends(get_db)) -> Item:
    item = await ItemRepository(db).get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


async def get_brand_or_404(brand_id: int, db: AsyncSession = Depends(get_db)) -> ItemBrand:
    brand = await ItemBrandRepository(db).get_by_id(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


async def get_category_or_404(category_id: int, db: AsyncSession = Depends(get_db)) -> ItemCategory:
    category = await ItemCategoryRepository(db).get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
