from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Product Schemas
class ProductCreate(BaseModel):
    product_id: str
    name: str
    available_stocks: int
    price_per_unit: float
    tax_percentage: float

class ProductResponse(ProductCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Bill Item Schemas
class BillItemCreate(BaseModel):
    product_id: str
    quantity: int

class BillItemResponse(BaseModel):
    id: int
    quantity: int
    unit_price: float
    tax_percentage: float
    item_subtotal: float
    item_tax: float
    item_total: float
    
    class Config:
        from_attributes = True

# Bill Schemas
class BillCreate(BaseModel):
    customer_email: EmailStr
    items: List[BillItemCreate]
    paid_amount: float

class BillResponse(BaseModel):
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

class CustomerPurchaseHistory(BaseModel):
    customer_email: str
    total_purchases: int
    bills: List[BillResponse]

# Denomination Schemas
class DenominationCreate(BaseModel):
    value: float

class DenominationResponse(DenominationCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
