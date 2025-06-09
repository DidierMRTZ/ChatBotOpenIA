from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float, DateTime
from config.Database import engine, Base
from datetime import datetime

class Sale(Base):
    __tablename__ = 'tb_sales'
    saleId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Información básica de la venta
    referenceNumber = Column(String(100), unique=True, nullable=False)
    saleDate = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    clientId = Column(Integer, ForeignKey("tb_clients.clientId"), nullable=False)
    invoiceId = Column(Integer, ForeignKey("tb_invoices.invoiceId"), nullable=True)
    
    # Detalles financieros
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0.16)
    discount = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    
    # Timestamps
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
