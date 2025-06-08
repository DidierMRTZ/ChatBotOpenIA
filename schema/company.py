from pydantic import BaseModel
from typing import Optional
# from datetime import datetime # No longer needed if createdAt/updatedAt are not used by CompanyBase

class CompanyBase(BaseModel):
    companyName: str  # Not optional as nullable=False in model
    companyEmail: Optional[str] = None
    companyPhone: Optional[str] = None
    companyWebsite: Optional[str] = None
    address: Optional[str] = None
    # firstName and lastName removed

    class Config:
        from_attributes = True

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    companyId: int
    # createdAt and updatedAt are not in the current model,
    # but keeping them here if they are intended for future use or were from a previous version.
    # If not, they can be removed.
    # createdAt: Optional[datetime] = None 
    # updatedAt: Optional[datetime] = None

class CompanyUpdate(CompanyBase):
    # Similar to CompanyRead, createdAt and updatedAt are not in the current Company model.
    # If these are not meant to be updatable or part of the company data, they can be removed.
    # createdAt: Optional[datetime] = None
    # updatedAt: Optional[datetime] = None
    pass
