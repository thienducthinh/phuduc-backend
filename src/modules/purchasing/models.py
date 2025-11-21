from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.core.database import Base


class Supplier(Base):
    __tablename__ = "supplier"
    supplier_id      = Column(Integer, primary_key=True, index=True)
    supplier_name    = Column(String(255))
    supplier_address = Column(String(255))
    supplier_phone   = Column(String(15))
    supplier_email   = Column(String(100))

    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")


class PurchaseOrder(Base):
    __tablename__ = "purchase_order"
    purchase_order_id = Column(Integer, ForeignKey("inventory_transaction.transaction_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    supplier_id       = Column(Integer, ForeignKey("supplier.supplier_id", ondelete="CASCADE", onupdate="CASCADE"))
    order_date        = Column(DateTime, server_default=func.now())

    supplier    = relationship("Supplier", back_populates="purchase_orders")
    transaction = relationship("InventoryTransaction")
