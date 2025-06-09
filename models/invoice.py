from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float, DateTime
from config.Database import engine, Base
from datetime import datetime




class Invoice(Base): # Changed from Factura
    __tablename__ = 'tb_invoices' # Changed from tb_facturas
    invoiceId = Column(Integer, primary_key=True, autoincrement=True)
    
    # Información básica
    invoiceNumber = Column(String(100), unique=True, nullable=False)  # Número de factura único
    issueDate = Column(DateTime, default=datetime.utcnow)  # Fecha de emisión
    dueDate = Column(DateTime, nullable=True)  # Fecha de vencimiento

    # Relación con cliente o compañía (asumimos que está relacionado con tb_company)
    companyId = Column(Integer, ForeignKey("tb_companies.companyId"), nullable=False)
    # Relación con cliente o compañía (asumimos que está relacionado con tb_company)
    clientId = Column(Integer, ForeignKey("tb_clients.clientId"), nullable=False)


    # Estado de la factura
    status = Column(String(50), default="pendiente")  # Ej: pendiente, pagada, cancelada

    # Timestamps
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#    # Totales
#    subtotal = Column(Float, nullable=False)
#    quantity = Column(Integer, nullable=False)
#    total = Column(Float, nullable=False)