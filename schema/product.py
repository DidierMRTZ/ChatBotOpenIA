from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    sku: Optional[str] = None
    price: Optional[int] = None
    stock: Optional[int] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    isActive: Optional[bool] = None

    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    productId: int

class ProductUpdate(ProductBase):
    pass
