from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .models import Item
from .schemas import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse
from .service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


def get_db():
    """Dependency for database session - adjust based on your setup"""
    pass


@router.get("/", response_model=ItemListResponse)
def list_items(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """List all items with pagination"""
    items = ItemService.get_items(db, skip=skip, limit=limit)
    total = ItemService.get_items_count(db)
    page = skip // limit + 1
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": limit,
    }


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a single item by ID"""
    item = ItemService.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item"""
    return ItemService.create_item(db, item)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
):
    """Update an item"""
    item = ItemService.update_item(db, item_id, item_update)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item"""
    success = ItemService.delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None


@router.get("/search/", response_model=list[ItemResponse])
def search_items(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """Search items by name"""
    return ItemService.search_items(db, q, skip=skip, limit=limit)
