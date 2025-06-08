from fastapi import APIRouter, HTTPException
from config.Database import engine, func
from sqlalchemy.orm import sessionmaker
from models.company import Company
from typing import List # Optional might not be needed directly here. BaseModel import removed as not directly used.
from schema.company import CompanyCreate, CompanyUpdate, CompanyRead
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK

company = APIRouter()

@company.get('/companies', status_code=HTTP_200_OK, response_model=List[CompanyRead])
def get_companies():
    Session = sessionmaker(bind=engine)
    session = Session()
    companies_list = session.query(Company).all() # Renamed variable for clarity
    session.close()
    return companies_list

@company.get('/companies/{companyId}', status_code=HTTP_200_OK, response_model=CompanyRead)
def get_companies_id(companyId: int):
    Session = sessionmaker(bind=engine)
    db = Session()
    company_record = db.query(Company).filter(Company.companyId == companyId).first()
    db.close()
    if not company_record:
        raise HTTPException(status_code=404, detail="Compañía no encontrada")
    return company_record

@company.post('/companies', status_code=HTTP_201_CREATED, response_model=CompanyRead)
def create_companies(company_data: CompanyCreate): # company_data will use new schema
    Session = sessionmaker(bind=engine)
    session = Session()
    new_company = Company(**company_data.dict()) # Model expects new fields
    session.add(new_company)
    session.commit()
    session.refresh(new_company)
    session.close()
    return new_company

@company.delete('/companies/{companyId}', status_code=HTTP_204_NO_CONTENT)
def delete_companies_id(companyId: int):
    Session = sessionmaker(bind=engine)
    db = Session()
    company_to_delete = db.query(Company).filter(Company.companyId == companyId).first()
    if not company_to_delete:
        db.close()
        raise HTTPException(status_code=404, detail="Compañía no encontrada")
    db.delete(company_to_delete)
    db.commit()
    db.close()
    return {"message": "Compañía eliminada correctamente"}

@company.put('/companies/{companyId}', status_code=HTTP_200_OK, response_model=CompanyRead)
def update_companies(companyId: int, company_update: CompanyUpdate): # company_update uses new schema
    Session = sessionmaker(bind=engine)
    db = Session()
    company_record = db.query(Company).filter(Company.companyId == companyId).first()
    if not company_record:
        db.close()
        raise HTTPException(status_code=404, detail="Compañía no encontrada")
    
    for key, value in company_update.dict(exclude_unset=True).items():
        setattr(company_record, key, value)
    db.commit()
    db.refresh(company_record)
    db.close()
    return company_record

@company.get('/queryCompanyInfo', status_code=HTTP_200_OK)
def get_companies_summary(): # Renamed function
    Session = sessionmaker(bind=engine)
    db = Session()
    # Updated query to group by address and count companies.
    # Returns a list of tuples/objects: (address, company_count)
    data = db.query(
        Company.address,
        func.count(Company.companyId).label('company_count')
    ).group_by(Company.address).all()
    db.close()
    # Note: The response_model for this endpoint is not explicitly defined.
    # The result will be a list of records, e.g., [Row(address='123 Main St', company_count=5), ...]
    return data
