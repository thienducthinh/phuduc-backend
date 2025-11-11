from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os

Base = declarative_base()

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  # Format: mssql+pyodbc

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    price = Column(Float)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    supplier = Column(String(100))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer)
    item = relationship("Item")

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String(100))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer)
    item = relationship("Item")

# For local SQLite
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)