from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from .models import PriceBook
from .repository import PriceBookRepository


async def get_price_book_or_404(price_book_id: int, db: AsyncSession = Depends(get_db)) -> PriceBook:
    entry = await PriceBookRepository(db).get_by_id(price_book_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Price book entry not found")
    return entry
