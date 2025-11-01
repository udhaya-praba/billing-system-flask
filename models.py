from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    available_stocks = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bill_items = relationship("BillItem", back_populates="product")

class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(String(50), unique=True, nullable=False)
    customer_email = Column(String(255), nullable=False)
    subtotal = Column(Float, nullable=False)
    total_tax = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    balance_amount = Column(Float, nullable=False)
    balance_denominations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bill_items = relationship("BillItem", back_populates="bill")

class BillItem(Base):
    __tablename__ = "bill_items"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)
    item_subtotal = Column(Float, nullable=False)
    item_tax = Column(Float, nullable=False)
    item_total = Column(Float, nullable=False)
    
    bill = relationship("Bill", back_populates="bill_items")
    product = relationship("Product", back_populates="bill_items")

class Denomination(Base):
    __tablename__ = "denominations"
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
