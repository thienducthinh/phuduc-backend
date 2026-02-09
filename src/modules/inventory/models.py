from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum, func
from sqlalchemy.orm import relationship
from src.core.database import Base


class Warehouse(Base):
    __tablename__ = "warehouse"
    warehouse_id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String(255))
    warehouse_address = Column(String(255))

    inventory_transactions = relationship("InventoryTransaction", back_populates="warehouse")


class InventoryTransaction(Base):
    __tablename__ = "inventory_transaction"
    transaction_id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.warehouse_id", ondelete="CASCADE", onupdate="CASCADE"))
    transaction_type = Column(Enum('Purchase Order', 'Sales Order', name='transaction_type_enum'), nullable=False)
    total_amount = Column(Numeric(10, 2))
    transaction_date = Column(DateTime, server_default=func.now())

    warehouse = relationship("Warehouse", back_populates="inventory_transactions")
    transaction_lines = relationship("InventoryTransactionLine", back_populates="transaction")


class InventoryTransactionLine(Base):
    __tablename__ = "inventory_transaction_line"
    line_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("inventory_transaction.transaction_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_id = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"))
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2))
    total_amount = Column(Numeric(10, 2))

    transaction = relationship("InventoryTransaction", back_populates="transaction_lines")
