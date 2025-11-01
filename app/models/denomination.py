"""
Denomination models
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Denomination(Base):
    """Denomination model for storing available denominations"""
    
    __tablename__ = "denominations"
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    denominations_used = relationship("DenominationUsed", back_populates="denomination", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Denomination(value={self.value})>"


class DenominationUsed(Base):
    """DenominationUsed model for tracking denominations used in bills"""
    
    __tablename__ = "denominations_used"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False, index=True)
    denomination_id = Column(Integer, ForeignKey("denominations.id"), nullable=False, index=True)
    count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    bill = relationship("Bill", back_populates="denominations_used")
    denomination = relationship("Denomination", back_populates="denominations_used")
    
    def __repr__(self):
        return f"<DenominationUsed(bill_id={self.bill_id}, denomination_id={self.denomination_id}, count={self.count})>"
