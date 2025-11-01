"""
Product model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Product(Base):
    """Product model for storing product information"""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    available_stocks = Column(Integer, nullable=False, default=0)
    price_per_unit = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bill_items = relationship("BillItem", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(product_id={self.product_id}, name={self.name})>"
