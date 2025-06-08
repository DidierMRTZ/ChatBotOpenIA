from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConversationCreate(BaseModel):
    CreationTimestamp: Optional[datetime] = None
    CreatedBy: Optional[str] = None
    ModificationTimestamp: Optional[datetime] = None
    ModifiedBy: Optional[str] = None
    CommetCpt: Optional[str] = None
    CommetUser: Optional[str] = None
    TextCommet: Optional[str] = None
    ChatId: Optional[int] = None

class ConversationUpdate(BaseModel):
    CreationTimestamp: Optional[datetime] = None
    CreatedBy: Optional[str] = None
    ModificationTimestamp: Optional[datetime] = None
    ModifiedBy: Optional[str] = None
    CommetCpt: Optional[str] = None
    CommetUser: Optional[str] = None
    TextCommet: Optional[str] = None
    ChatId: Optional[int] = None
