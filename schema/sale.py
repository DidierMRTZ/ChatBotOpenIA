from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SaleBase(BaseModel):
    referenceNumber: Optional[str] = None
    saleDate: Optional[datetime] = None
    clientId: Optional[int] = None
    invoiceId: Optional[int] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = 0.16
    discount: Optional[float] = 0.0
    total: Optional[float] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True  # Para compatibilidad con ORM en Pydantic v2

class SaleCreate(SaleBase):
    pass

class SaleRead(SaleBase):
    saleId: int

class SaleUpdate(SaleBase):
    pass
