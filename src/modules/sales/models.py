from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.modules.customer.models import Customer


class SalesOrder(Base):
    __tablename__ = "sales_order"
    sales_order_id = Column(Integer, ForeignKey("inventory_transaction.transaction_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    customer_id    = Column(Integer, ForeignKey("customer.customer_id", ondelete="CASCADE", onupdate="CASCADE"))
    order_date     = Column(DateTime, server_default=func.now())

    customer    = relationship("Customer", back_populates="sales_orders")
    transaction = relationship("InventoryTransaction")
