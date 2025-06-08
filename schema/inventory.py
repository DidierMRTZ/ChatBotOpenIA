from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InventoryBase(BaseModel): # Changed from UserBase
    inventoryId: Optional[int] = None
    productId: Optional[int] = None
    companyId: Optional[int] = None
    quantity: Optional[int] = None
    costPrice: Optional[float] = None
    salePrice: Optional[float] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


    class Config:
        from_attributes = True # For Pydantic v2 ORM compatibility

class InventoryCreate(InventoryBase): # Changed from UserCreate
    pass

class InventoryRead(InventoryBase): # Changed from UserRead
    inventoryId: int # Changed from userId

class InventoryUpdate(InventoryBase): # Changed from UserUpdate
    pass
