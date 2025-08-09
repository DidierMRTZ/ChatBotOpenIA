from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.schema import Index
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
    
    __table_args__ = (
        Index("idx_fulltext_description", "description", mysql_prefix="FULLTEXT"),
        {},
    )
