"""
Bill and BillItem models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Bill(Base):
    """Bill model for storing billing information"""
    
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_email = Column(String(255), nullable=False, index=True)
    subtotal = Column(Float, nullable=False, default=0.0)
    total_tax = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    paid_amount = Column(Float, nullable=False, default=0.0)
    balance_amount = Column(Float, nullable=False, default=0.0)
    balance_denominations = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bill_items = relationship("BillItem", back_populates="bill", cascade="all, delete-orphan")
    denominations_used = relationship("DenominationUsed", back_populates="bill", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Bill(bill_number={self.bill_number}, customer_email={self.customer_email})>"


class BillItem(Base):
    """BillItem model for storing individual items in a bill"""
    
    __tablename__ = "bill_items"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)
    item_subtotal = Column(Float, nullable=False)
    item_tax = Column(Float, nullable=False)
    item_total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    bill = relationship("Bill", back_populates="bill_items")
    product = relationship("Product", back_populates="bill_items")
    
    def __repr__(self):
        return f"<BillItem(bill_id={self.bill_id}, product_id={self.product_id}, quantity={self.quantity})>"
