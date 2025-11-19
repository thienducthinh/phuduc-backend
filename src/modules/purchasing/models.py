from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id        = Column(Integer, primary_key=True, index=True)
    supplier  = Column(String(100))


class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"
    id              = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"))
    # item_id         = Column(Integer, ForeignKey("items.id"))
    quantity        = Column(Integer)
    purchase_order  = relationship("PurchaseOrder", back_populates="line_items")
    # item            = relationship("Item")