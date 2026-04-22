from datetime import datetime
from sqlalchemy import Column, Integer, SmallInteger, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.core.database import Base


# Association table for many-to-many relationship between Item and ItemCategory
item_category_association = Table(
    "item_category_association",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("item_category.category_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


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

    items = relationship("Item", secondary=item_category_association, back_populates="categories")


class Item(Base):
    __tablename__ = "item"
    item_id          = Column(Integer, primary_key=True, index=True)
    brand_id         = Column(SmallInteger, ForeignKey("item_brand.brand_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_name        = Column(String(255), nullable=False)
    item_description = Column(Text)

    brand      = relationship("ItemBrand", back_populates="items")
    categories = relationship("ItemCategory", secondary=item_category_association, back_populates="items")
