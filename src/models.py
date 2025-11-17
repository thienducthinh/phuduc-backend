import os
from dotenv import load_dotenv

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from src.core.database import Base, engine, AsyncSessionLocal

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")   # <-- now a pymssql URL

# ------------------- MODELS -------------------
class Item(Base):
    __tablename__ = "items"
    id    = Column(Integer, primary_key=True, index=True)
    name  = Column(String(255), index=True)
    price = Column(Float)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id        = Column(Integer, primary_key=True, index=True)
    supplier  = Column(String(100))
    item_id   = Column(Integer, ForeignKey("items.id"))
    quantity  = Column(Integer)
    item      = relationship("Item")

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id        = Column(Integer, primary_key=True, index=True)
    customer  = Column(String(100))
    item_id   = Column(Integer, ForeignKey("items.id"))
    quantity  = Column(Integer)
    item      = relationship("Item")
# ---------------------------------------------

# ------------------- ENGINE -------------------
# engine = create_engine(
#     DATABASE_URL,
#     # optional but nice
#     pool_pre_ping=True,
#     echo=False,                 # set True if you want SQL logging
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables using async engine
async def init_db():
    """Initialize database tables - call this from FastAPI startup event"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created (or already exist).")
# ---------------------------------------------