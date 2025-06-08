from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatCreate(BaseModel):
    CreationTimestamp: Optional[datetime] = None
    CreatedBy: Optional[str] = None
    ModificationTimestamp: Optional[datetime] = None
    ModifiedBy: Optional[str] = None
    UserId: Optional[int] = None
    GptId: Optional[int] = None

class ChatUpdate(BaseModel):
    CreationTimestamp: Optional[datetime] = None
    CreatedBy: Optional[str] = None
    ModificationTimestamp: Optional[datetime] = None
    ModifiedBy: Optional[str] = None
    UserId: Optional[int] = None
    GptId: Optional[int] = None
