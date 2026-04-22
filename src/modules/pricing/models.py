from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DECIMAL, func
from sqlalchemy.orm import relationship
from src.core.database import Base


class PriceBook(Base):
    __tablename__ = "price_book"
    price_book_id      = Column(Integer, primary_key=True, index=True)
    business_id        = Column(Integer)
    description        = Column(String(255))
    price_type         = Column(Enum("Supplier", "Wholesale", "Retail", name="price_type_enum"), nullable=False)

    # Discount percentages
    discount_monthly   = Column(DECIMAL(5, 2), default=0)  # e.g., 5.00 for 5%
    discount_quarterly = Column(DECIMAL(5, 2), default=0)
    discount_yearly    = Column(DECIMAL(5, 2), default=0)

    lines = relationship("PriceBookLine", back_populates="price_book")


class PriceBookLine(Base):
    __tablename__ = "price_book_line"
    line_id       = Column(Integer, primary_key=True, index=True)
    price_book_id = Column(Integer, ForeignKey("price_book.price_book_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_id       = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"))
    price         = Column(DECIMAL(10, 2))

    price_book = relationship("PriceBook", back_populates="lines")
    item       = relationship("Item")
