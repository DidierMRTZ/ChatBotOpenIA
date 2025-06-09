from fastapi import APIRouter, HTTPException
from config.Database import engine, func
from sqlalchemy.orm import sessionmaker
from models.sale import Sale
from pydantic import BaseModel
from typing import Optional, List
from schema.sale import SaleCreate, SaleUpdate, SaleRead
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK

sale = APIRouter()

@sale.get('/sales', status_code=HTTP_200_OK, response_model=List[SaleRead])
def get_sales():
    Session = sessionmaker(bind=engine)
    session = Session()
    sales_list = session.query(Sale).all()
    session.close()
    return sales_list

@sale.get('/sales/{saleId}', status_code=HTTP_200_OK, response_model=SaleRead)
def get_sale_id(saleId: int):
    Session = sessionmaker(bind=engine)
    db = Session()
    sale_record = db.query(Sale).filter(Sale.saleId == saleId).first()
    db.close()
    if not sale_record:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale_record

@sale.post('/sales', status_code=HTTP_201_CREATED, response_model=SaleRead)
def create_sale(sale_data: SaleCreate):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_sale = Sale(**sale_data.dict())
    session.add(new_sale)
    session.commit()
    session.refresh(new_sale)
    session.close()
    return new_sale

@sale.delete('/sales/{saleId}', status_code=HTTP_204_NO_CONTENT)
def delete_sale(saleId: int):
    Session = sessionmaker(bind=engine)
    db = Session()
    sale_to_delete = db.query(Sale).filter(Sale.saleId == saleId).first()
    if not sale_to_delete:
        db.close()
        raise HTTPException(status_code=404, detail="Sale not found")
    db.delete(sale_to_delete)
    db.commit()
    db.close()
    return {"message": "Sale deleted successfully"}

@sale.put('/sales/{saleId}', status_code=HTTP_200_OK, response_model=SaleRead)
def update_sale(saleId: int, sale_update: SaleUpdate):
    Session = sessionmaker(bind=engine)
    db = Session()
    sale_record = db.query(Sale).filter(Sale.saleId == saleId).first()
    if not sale_record:
        db.close()
        raise HTTPException(status_code=404, detail="Sale not found")
    
    for key, value in sale_update.dict(exclude_unset=True).items():
        setattr(sale_record, key, value)
    db.commit()
    db.refresh(sale_record)
    db.close()
    return sale_record

@sale.get('/querySaleInfo', status_code=HTTP_200_OK)
def get_sales_summary():
    Session = sessionmaker(bind=engine)
    db = Session()
    data = db.query(
        Sale.saleId,
        Sale.referenceNumber,
        Sale.saleDate,
        Sale.clientId,
        Sale.invoiceId,
        Sale.subtotal,
        Sale.tax,
        Sale.discount,
        Sale.total,
        Sale.createdAt,
        Sale.updatedAt,
        func.count(Sale.saleId)
    ).group_by(Sale.saleId).all()
    db.close()
    return data
