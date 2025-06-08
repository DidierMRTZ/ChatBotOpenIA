from fastapi import APIRouter, HTTPException
from config.Database import engine, func
from sqlalchemy.orm import sessionmaker
from models.invoice import Invoice # Changed from Factura
from pydantic import BaseModel
from typing import Optional, List
from schema.invoice import InvoiceCreate, InvoiceUpdate, InvoiceRead # Changed from Factura schemas
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK

invoice = APIRouter() # Changed from factura

@invoice.get('/invoices', status_code=HTTP_200_OK, response_model=List[InvoiceRead]) # Path and response_model changed
def get_invoices(): # Renamed
    Session = sessionmaker(bind=engine)
    session = Session()
    invoices_list = session.query(Invoice).all() # Changed from Factura, variable 'invoices_list'
    session.close()
    return invoices_list

@invoice.get('/invoices/{invoiceId}', status_code=HTTP_200_OK, response_model=InvoiceRead) # Path, param, response_model changed
def get_invoices_id(invoiceId: int): # Renamed, param changed
    Session = sessionmaker(bind=engine)
    db = Session()
    invoice_record = db.query(Invoice).filter(Invoice.invoiceId == invoiceId).first() # Changed from Factura, facturaId. Variable 'invoice_record'
    db.close()
    if not invoice_record:
        raise HTTPException(status_code=404, detail="Invoice not found") # Message changed
    return invoice_record

@invoice.post('/invoices', status_code=HTTP_201_CREATED, response_model=InvoiceRead) # Path and response_model changed
def create_invoices(invoice_data: InvoiceCreate): # Renamed, param type changed. Variable 'invoice_data'
    Session = sessionmaker(bind=engine)
    session = Session()
    new_invoice = Invoice(**invoice_data.dict()) # Changed from Factura. Variable 'new_invoice'
    session.add(new_invoice)
    session.commit()
    session.refresh(new_invoice)
    session.close()
    return new_invoice

@invoice.delete('/invoices/{invoiceId}', status_code=HTTP_204_NO_CONTENT) # Path and param changed
def delete_invoices_id(invoiceId: int): # Renamed, param changed
    Session = sessionmaker(bind=engine)
    db = Session()
    invoice_to_delete = db.query(Invoice).filter(Invoice.invoiceId == invoiceId).first() # Changed from Factura, facturaId. Variable 'invoice_to_delete'
    if not invoice_to_delete:
        db.close()
        raise HTTPException(status_code=404, detail="Invoice not found") # Message changed
    db.delete(invoice_to_delete)
    db.commit()
    db.close()
    return {"message": "Invoice deleted successfully"} # Message changed

@invoice.put('/invoices/{invoiceId}', status_code=HTTP_200_OK, response_model=InvoiceRead) # Path, param, response_model changed
def update_invoices(invoiceId: int, invoice_update: InvoiceUpdate): # Renamed, params changed. Variable 'invoice_update'
    Session = sessionmaker(bind=engine)
    db = Session()
    invoice_record = db.query(Invoice).filter(Invoice.invoiceId == invoiceId).first() # Changed from Factura, facturaId. Variable 'invoice_record'
    if not invoice_record:
        db.close()
        raise HTTPException(status_code=404, detail="Invoice not found") # Message changed
    
    for key, value in invoice_update.dict(exclude_unset=True).items():
        setattr(invoice_record, key, value)
    db.commit()
    db.refresh(invoice_record)
    db.close()
    return invoice_record

@invoice.get('/queryInvoiceInfo', status_code=HTTP_200_OK) # Path changed
def get_invoices_summary(): # Renamed
    Session = sessionmaker(bind=engine)
    db = Session()
    # Query adjusted for Invoice model
    data = db.query(
        Invoice.firstName, 
        Invoice.lastName, 
        func.count(Invoice.invoiceId) # Changed from Factura.facturaId
    ).group_by(Invoice.firstName, Invoice.lastName).all()
    db.close()
    return data
