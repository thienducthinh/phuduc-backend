from sqlalchemy import Column, Integer, String, Text, Float, DECIMAL, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from src.core.database import Base


class ItemBrand(Base):
    __tablename__ = "item_brand"
    brand_id          = Column(Integer, primary_key=True, index=True)
    brand_name        = Column(String(255), nullable=False)
    brand_description = Column(Text)

    items = relationship("Item", back_populates="brand")


class ItemCategory(Base):
    __tablename__ = "item_category"
    category_id          = Column(Integer, primary_key=True, index=True)
    category_name        = Column(String(255), nullable=False)
    category_description = Column(Text)

    items = relationship("Item", back_populates="category")


class Item(Base):
    __tablename__ = "item"
    item_id          = Column(Integer, primary_key=True, index=True)
    brand_id         = Column(Integer, ForeignKey("item_brand.brand_id", ondelete="CASCADE", onupdate="CASCADE"))
    category_id      = Column(Integer, ForeignKey("item_category.category_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_name        = Column(String(255), nullable=False)
    item_description = Column(Text)

    brand    = relationship("ItemBrand", back_populates="items")
    category = relationship("ItemCategory", back_populates="items")


class Warehouse(Base):
    __tablename__ = "warehouse"
    warehouse_id   = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String(255))

    inventories  = relationship("Inventory", back_populates="warehouse")
    transactions = relationship("InventoryTransaction", back_populates="warehouse")


class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id = Column(Integer, primary_key=True, index=True)
    item_id      = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"))
    warehouse_id = Column(Integer, ForeignKey("warehouse.warehouse_id", ondelete="CASCADE", onupdate="CASCADE"))
    quantity     = Column(Integer, nullable=False)

    item      = relationship("Item")
    warehouse = relationship("Warehouse", back_populates="inventories")


class InventoryTransaction(Base):
    __tablename__ = "inventory_transaction"
    transaction_id   = Column(Integer, primary_key=True, index=True)
    warehouse_id     = Column(Integer, ForeignKey("warehouse.warehouse_id", ondelete="CASCADE", onupdate="CASCADE"))
    transaction_type = Column(Enum("Purchase Order", "Sales Order", name="transaction_type_enum"), nullable=False)
    total_amount     = Column(DECIMAL(10, 2))
    transaction_date = Column(DateTime, server_default=func.now())

    warehouse = relationship("Warehouse", back_populates="transactions")
    lines     = relationship("InventoryTransactionLine", back_populates="transaction")


class InventoryTransactionLine(Base):
    __tablename__ = "inventory_transaction_line"
    line_id        = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("inventory_transaction.transaction_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_id        = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"))
    quantity       = Column(Integer, nullable=False)
    price          = Column(DECIMAL(10, 2))
    total_amount   = Column(DECIMAL(10, 2))

    transaction = relationship("InventoryTransaction", back_populates="lines")
    item        = relationship("Item")


class PriceBook(Base):
    __tablename__ = "price_book"
    price_book_id = Column(Integer, primary_key=True, index=True)
    business_id   = Column(Integer)
    description   = Column(String(255))
    price_type    = Column(Enum("Supplier", "Wholesale", "Retail", name="price_type_enum"), nullable=False)

    lines = relationship("PriceBookLine", back_populates="price_book")


class PriceBookLine(Base):
    __tablename__ = "price_book_line"
    line_id       = Column(Integer, primary_key=True, index=True)
    price_book_id = Column(Integer, ForeignKey("price_book.price_book_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_id       = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"))
    price         = Column(DECIMAL(10, 2))

    price_book = relationship("PriceBook", back_populates="lines")
    item       = relationship("Item")


class InventoryAdjustment(Base):
    __tablename__ = "inventory_adjustment"
    adjustment_id   = Column(Integer, ForeignKey("inventory_transaction.transaction_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    adjustment_date = Column(DateTime, server_default=func.now())

    transaction = relationship("InventoryTransaction")
