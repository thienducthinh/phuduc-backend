from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from src.core.database import Base


class Carrier(Base):
    __tablename__ = "carrier"

    carrier_id    = Column(Integer, primary_key=True, index=True)
    carrier_name  = Column(String(255), nullable=False)
    carrier_phone = Column(String(50))
    carrier_email = Column(String(100))

    deliveries = relationship("Delivery", back_populates="carrier")


class Delivery(Base):
    __tablename__ = "delivery"

    delivery_id      = Column(Integer, primary_key=True, index=True)
    sales_order_id   = Column(Integer, ForeignKey("sales_order.sales_order_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    carrier_id       = Column(Integer, ForeignKey("carrier.carrier_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    delivery_address = Column(String(500), nullable=False)
    scheduled_date   = Column(Date, nullable=False)
    delivered_date   = Column(Date, nullable=True)
    status           = Column(
        Enum("Pending", "In Transit", "Delivered", "Failed", name="delivery_status_enum"),
        nullable=False,
        default="Pending",
    )
    tracking_number  = Column(String(100), nullable=True)

    carrier     = relationship("Carrier", back_populates="deliveries")
    sales_order = relationship("SalesOrder")
