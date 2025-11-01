"""
Denomination schemas for request/response validation
"""
from pydantic import BaseModel, Field
from datetime import datetime


class DenominationBase(BaseModel):
    """Base denomination schema"""
    value: float = Field(..., gt=0)


class DenominationCreate(DenominationBase):
    """Schema for creating a denomination"""
    pass


class DenominationResponse(DenominationBase):
    """Schema for denomination response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DenominationListResponse(BaseModel):
    """Schema for denomination list response"""
    total: int
    items: list[DenominationResponse]
