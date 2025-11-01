"""
Bill schemas for request/response validation
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


class BillItemCreate(BaseModel):
    """Schema for creating a bill item"""
    product_id: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class BillItemResponse(BaseModel):
    """Schema for bill item response"""
    id: int
    product_id: int
    quantity: int
    unit_price: float
    tax_percentage: float
    item_subtotal: float
    item_tax: float
    item_total: float
    
    class Config:
        from_attributes = True


class DenominationInput(BaseModel):
    """Schema for denomination input"""
    denomination_value: float = Field(..., gt=0)
    count: int = Field(..., ge=0)


class BillCreate(BaseModel):
    """Schema for creating a bill"""
    customer_email: EmailStr
    items: List[BillItemCreate] = Field(..., min_items=1)
    paid_amount: float = Field(..., gt=0)
    denominations_received: Optional[List[DenominationInput]] = None


class BillResponse(BaseModel):
    """Schema for bill response"""
    id: int
    bill_number: str
    customer_email: str
    subtotal: float
    total_tax: float
    total_amount: float
    paid_amount: float
    balance_amount: float
    balance_denominations: Optional[str]
    created_at: datetime
    bill_items: List[BillItemResponse]
    
    class Config:
        from_attributes = True


class BillListResponse(BaseModel):
    """Schema for bill list response"""
    total: int
    items: List[BillResponse]


class BillDetailResponse(BillResponse):
    """Schema for detailed bill response"""
    pass


class CustomerPurchaseHistoryResponse(BaseModel):
    """Schema for customer purchase history"""
    customer_email: str
    total_purchases: int
    bills: List[BillResponse]
