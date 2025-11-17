from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from src.models import PurchaseOrder, SalesOrder, Item
from src.core.database import AsyncSessionLocal

router = APIRouter()

class POCreate(BaseModel):
    supplier: str
    item_id: int
    quantity: int

class SOCreate(BaseModel):
    customer: str
    item_id: int
    quantity: int

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

@router.post("/po/")
async def create_po(po: POCreate, db: AsyncSession = Depends(get_db)):
    db_po = PurchaseOrder(supplier=po.supplier, item_id=po.item_id, quantity=po.quantity)
    db.add(db_po)
    await db.commit()
    await db.refresh(db_po)
    return db_po

@router.get("/po/{po_id}")
async def read_po(po_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(PurchaseOrder).filter(PurchaseOrder.id == po_id))
    po = result.scalar_one_or_none()
    if po is None:
        raise HTTPException(status_code=404, detail="PO not found")
    return po

# Similar for SO: create_so, read_so
# Add for items: create_item, etc.