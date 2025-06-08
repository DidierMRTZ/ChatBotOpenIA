from pydantic import BaseModel
from typing import Optional

class ClientBase(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None

    class Config:
        orm_mode = True

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    clientId: int

class ClientUpdate(ClientBase):
    pass
