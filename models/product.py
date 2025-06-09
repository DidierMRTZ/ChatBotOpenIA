from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from config.Database import engine, Base

class Product(Base):
    __tablename__ = 'tb_products'
    productId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sku = Column(String(255), nullable=True)
    price = Column(Integer, nullable=True)
    stock = Column(Integer, nullable=True)  
    description = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    brand = Column(String(255), nullable=True)
    isActive = Column(Boolean, nullable=True)

# Crear tablas
Base.metadata.create_all(engine)