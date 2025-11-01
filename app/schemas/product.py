"""
Product schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """Base product schema"""
    product_id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    available_stocks: int = Field(..., ge=0)
    price_per_unit: float = Field(..., gt=0)
    tax_percentage: float = Field(default=0.0, ge=0, le=100)


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    available_stocks: Optional[int] = Field(None, ge=0)
    price_per_unit: Optional[float] = Field(None, gt=0)
    tax_percentage: Optional[float] = Field(None, ge=0, le=100)


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for product list response"""
    total: int
    items: list[ProductResponse]
