from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InvoiceBase(BaseModel): # Changed from FacturaBase
    invoiceNumber: Optional[str] = None
    issueDate: Optional[datetime] = None
    dueDate: Optional[datetime] = None
    companyId: Optional[int] = None
    clientId: Optional[int] = None
    status: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


    class Config:
        from_attributes = True # For Pydantic v2 ORM compatibility

class InvoiceCreate(InvoiceBase): # Changed from FacturaCreate
    pass

class InvoiceRead(InvoiceBase): # Changed from FacturaRead
    invoiceId: int # Changed from facturaId

class InvoiceUpdate(InvoiceBase): # Changed from FacturaUpdate
    pass
