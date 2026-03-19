from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from .dependencies import get_price_book_or_404
from .models import PriceBook
from .schemas import PriceBookCreate, PriceBookUpdate, PriceBookResponse
from .service import PriceBookService

router = APIRouter(prefix="/price-book", tags=["Price Book"])


@router.get("/", response_model=list[PriceBookResponse])
async def list_price_book(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    return await PriceBookService(db).get_all(skip=skip, limit=limit)


@router.get("/item/{item_id}", response_model=list[PriceBookResponse])
async def list_by_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await PriceBookService(db).get_by_item(item_id)


@router.get("/{price_book_id}", response_model=PriceBookResponse)
async def get_price_book(entry: PriceBook = Depends(get_price_book_or_404)):
    return entry


@router.post("/", response_model=PriceBookResponse, status_code=201)
async def create_price_book(data: PriceBookCreate, db: AsyncSession = Depends(get_db)):
    return await PriceBookService(db).create(data)


@router.put("/{price_book_id}", response_model=PriceBookResponse)
async def update_price_book(
    data: PriceBookUpdate,
    entry: PriceBook = Depends(get_price_book_or_404),
    db: AsyncSession = Depends(get_db),
):
    return await PriceBookService(db).update(entry, data)


@router.delete("/{price_book_id}", status_code=204)
async def delete_price_book(
    entry: PriceBook = Depends(get_price_book_or_404),
    db: AsyncSession = Depends(get_db),
):
    await PriceBookService(db).delete(entry)
