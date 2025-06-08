from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config.Database import engine

# Definir base y modelo
Base = declarative_base()

class Invoice(Base): # Changed from Factura
    __tablename__ = 'tb_invoices' # Changed from tb_facturas
    invoiceId = Column(Integer, primary_key=True, index=True, autoincrement=True) # Changed from facturaId
    firstName = Column(String(255), nullable=True) # Kept as per user model
    lastName = Column(String(255), nullable=True)  # Kept as per user model

# Crear tablas
Base.metadata.create_all(bind=engine)
