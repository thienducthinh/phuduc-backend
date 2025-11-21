from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.modules.purchasing.models import PurchaseOrder
from src.modules.purchasing.schemas import POCreate

router = APIRouter(prefix="/po", tags=["Purchasing"])


@router.post("/")
async def create_po(po: POCreate, db: AsyncSession = Depends(get_db)):
    db_po = PurchaseOrder(supplier_id=po.supplier_id)
    db.add(db_po)
    await db.commit()
    await db.refresh(db_po)
    return db_po


@router.get("/{po_id}")
async def read_po(po_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PurchaseOrder).filter(PurchaseOrder.purchase_order_id == po_id))
    po = result.scalar_one_or_none()
    if po is None:
        raise HTTPException(status_code=404, detail="PO not found")
    return po
