from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer,Float, DateTime
from datetime import datetime
from config.Database import engine, Base

class Inventory(Base): # Changed from User
    __tablename__ = 'tb_inventories' # Changed from tb_users
    inventoryId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    productId = Column(Integer, ForeignKey("tb_products.productId"))
    companyId = Column(Integer, ForeignKey("tb_companies.companyId"))

    quantity = Column(Integer, default=0)
    costPrice = Column(Float)
    salePrice = Column(Float)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


