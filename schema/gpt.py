from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GptCreate(BaseModel):
    CreationTimestamp: Optional[datetime] = None
    CreatedBy: str
    ModificationTimestamp: Optional[datetime] = None
    ModifiedBy: str
    AsistentId: str

class GptUpdate(BaseModel):
    CreationTimestamp: Optional[datetime] = None
    CreatedBy: Optional[str] = None
    ModificationTimestamp: Optional[datetime] = None
    ModifiedBy: Optional[str] = None
    AsistentId: Optional[str] = None
