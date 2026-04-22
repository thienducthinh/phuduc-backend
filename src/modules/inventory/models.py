from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum, func
from sqlalchemy.orm import relationship
from src.core.database import Base


class Warehouse(Base):
    __tablename__ = "warehouse"
    warehouse_id      = Column(Integer, primary_key=True, index=True)
    warehouse_name    = Column(String(255))
    warehouse_address = Column(String(255))

    inventory_transactions = relationship("InventoryTransaction", back_populates="warehouse")
    inventories            = relationship("Inventory", back_populates="warehouse")


class Inventory(Base):
    __tablename__ = "inventory"
    item_id      = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.warehouse_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    quantity     = Column(Integer, nullable=False, default=0)

    item      = relationship("Item")
    warehouse = relationship("Warehouse", back_populates="inventories")


class InventoryTransaction(Base):
    __tablename__ = "inventory_transaction"
    transaction_id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.warehouse_id", ondelete="CASCADE", onupdate="CASCADE"))
    transaction_type = Column(Enum('Purchase Order', 'Sales Order', name='transaction_type_enum'), nullable=False)
    total_amount = Column(Numeric(10, 2))
    transaction_date = Column(DateTime, server_default=func.now())

    warehouse         = relationship("Warehouse", back_populates="inventory_transactions")
    transaction_lines = relationship("InventoryTransactionLine", back_populates="transaction")
    purchase_order    = relationship("PurchaseOrder", back_populates="transaction", uselist=False)
    sales_order       = relationship("SalesOrder", back_populates="transaction", uselist=False)


class InventoryTransactionLine(Base):
    __tablename__ = "inventory_transaction_line"
    line_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("inventory_transaction.transaction_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_id = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"))
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2))
    total_amount = Column(Numeric(10, 2))

    transaction = relationship("InventoryTransaction", back_populates="transaction_lines")
    item        = relationship("Item")
<<<<<<< HEAD


class InventoryAdjustment(Base):
    __tablename__ = "inventory_adjustment"
    adjustment_id   = Column(Integer, ForeignKey("inventory_transaction.transaction_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    adjustment_date = Column(DateTime, server_default=func.now())

    transaction = relationship("InventoryTransaction")
=======
>>>>>>> f391c95de8514382ab825e03c3b06b3c6cba6114
