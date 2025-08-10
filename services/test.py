from sqlalchemy import create_engine, MetaData, func
import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import event, text as sql_text
from sqlalchemy.schema import DDL

# Configurar conexión a MySQL
# Usar el nombre del servicio de Docker para el host
db_host = os.environ.get('DB_HOST', 'db')  # Por defecto 'db' para Docker
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/nudges"
#DATABASE_URL = f"mysql+pymysql://username:password@db:3306/nudges" #para localhost 
engine = create_engine(DATABASE_URL)
Base = declarative_base()

event.listen(
    Base.metadata,
    "after_create",
    DDL("ALTER TABLE tb_products ADD FULLTEXT INDEX idx_fulltext_description (description)")
)

from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String, Boolean

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


from sqlalchemy import select, desc
from sqlalchemy.dialects.mysql import match
from sqlalchemy.orm import Session

stmt = select(Product).where(
    match(Product.description, against='+arroz +leche +pan')
)

with Session(engine) as session:
    results = session.execute(stmt).scalars().all()

for product in results:
    print(f"Product ID: {product.productId}, Description: {product.description}")
  