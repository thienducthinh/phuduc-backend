from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from src.core.database import Base


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_address = Column(String(255))
    customer_phone = Column(String(15))
    customer_email = Column(String(100))
    price_type = Column(
        Enum("Customer 1", "Customer 2", "Customer 3", name="customer_price_type_enum"),
        nullable=False
    )

    sales_orders = relationship("SalesOrder", back_populates="customer")
