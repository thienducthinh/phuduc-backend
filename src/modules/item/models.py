from datetime import datetime
from sqlalchemy import Column, Integer, SmallInteger, String, Text, DateTime, Boolean, ForeignKey
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
    brand_id         = Column(SmallInteger, ForeignKey("item_brand.brand_id", ondelete="CASCADE", onupdate="CASCADE"))
    category_id      = Column(SmallInteger, ForeignKey("item_category.category_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_name        = Column(String(255), nullable=False)
    item_description = Column(Text)

    brand    = relationship("ItemBrand", back_populates="items")
    category = relationship("ItemCategory", back_populates="items")
