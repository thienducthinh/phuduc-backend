from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id        = Column(Integer, primary_key=True, index=True)
    customer  = Column(String(100))
    item_id   = Column(Integer, ForeignKey("items.id"))
    quantity  = Column(Integer)
    item      = relationship("Item")
