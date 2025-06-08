from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    userId: int

class UserUpdate(UserBase):
    pass