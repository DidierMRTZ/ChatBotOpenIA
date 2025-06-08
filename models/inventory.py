from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer,Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from config.Database import engine
from datetime import datetime

# Definir base y modelo
Base = declarative_base()

class Inventory(Base): # Changed from User
    __tablename__ = 'tb_inventories' # Changed from tb_users
    inventoryId = Column(Integer, primary_key=True)
    productId = Column(Integer, ForeignKey("tb_products.productId"))
    companyId = Column(Integer, ForeignKey("tb_companies.companyId"))

    quantity = Column(Integer, default=0)
    costPrice = Column(Float)
    salePrice = Column(Float)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Crear tablas
Base.metadata.create_all(bind=engine)