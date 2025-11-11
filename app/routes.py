from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .models import SessionLocal, PurchaseOrder, SalesOrder, Item

router = APIRouter()

class POCreate(BaseModel):
    supplier: str
    item_id: int
    quantity: int

class SOCreate(BaseModel):
    customer: str
    item_id: int
    quantity: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/po/")
def create_po(po: POCreate, db: Session = Depends(get_db)):
    db_po = PurchaseOrder(supplier=po.supplier, item_id=po.item_id, quantity=po.quantity)
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    return db_po

@router.get("/po/{po_id}")
def read_po(po_id: int, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if po is None:
        raise HTTPException(status_code=404, detail="PO not found")
    return po

# Similar for SO: create_so, read_so
# Add for items: create_item, etc.