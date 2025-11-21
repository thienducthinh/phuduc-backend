from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.core.database import Base


class Customer(Base):
    __tablename__ = "customer"
    customer_id      = Column(Integer, primary_key=True, index=True)
    customer_name    = Column(String(255))
    customer_address = Column(String(255))
    customer_phone   = Column(String(15))
    customer_email   = Column(String(100))
    price_type       = Column(Enum("Customer 1", "Customer 2", "Customer 3", name="customer_price_type_enum"), nullable=False)

    sales_orders = relationship("SalesOrder", back_populates="customer")


class SalesOrder(Base):
    __tablename__ = "sales_order"
    sales_order_id = Column(Integer, ForeignKey("inventory_transaction.transaction_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    customer_id    = Column(Integer, ForeignKey("customer.customer_id", ondelete="CASCADE", onupdate="CASCADE"))
    order_date     = Column(DateTime, server_default=func.now())

    customer    = relationship("Customer", back_populates="sales_orders")
    transaction = relationship("InventoryTransaction")
