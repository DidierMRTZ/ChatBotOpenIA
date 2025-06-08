from pydantic import BaseModel
from typing import Optional

class InvoiceBase(BaseModel): # Changed from FacturaBase
    firstName: Optional[str] = None # Kept as per user model
    lastName: Optional[str] = None  # Kept as per user model

    class Config:
        from_attributes = True # For Pydantic v2 ORM compatibility

class InvoiceCreate(InvoiceBase): # Changed from FacturaCreate
    pass

class InvoiceRead(InvoiceBase): # Changed from FacturaRead
    invoiceId: int # Changed from facturaId

class InvoiceUpdate(InvoiceBase): # Changed from FacturaUpdate
    pass
