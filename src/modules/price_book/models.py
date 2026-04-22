from sqlalchemy import Column, Integer, ForeignKey, Numeric, Enum, Date, Boolean
from sqlalchemy.orm import relationship
from src.core.database import Base


class PriceBook(Base):
    __tablename__ = "price_book"

    price_book_id  = Column(Integer, primary_key=True, index=True)
    item_id        = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    price_type     = Column(
        Enum("Customer 1", "Customer 2", "Customer 3", name="customer_price_type_enum"),
        nullable=False
    )
    price          = Column(Numeric(12, 2), nullable=False)
    effective_date = Column(Date, nullable=False)
    expiry_date    = Column(Date, nullable=True)
    is_active      = Column(Boolean, default=True, nullable=False)

    item = relationship("Item")
