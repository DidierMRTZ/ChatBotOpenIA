from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String # Removed unused Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from config.Database import engine

# Definir base y modelo
Base = declarative_base()

class Company(Base):
    __tablename__ = 'tb_companies'
    companyId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    companyName = Column(String(255), nullable=False)  # nombre único
    companyEmail = Column(String(255), nullable=True)  # opcional: email único
    companyPhone = Column(String(50), nullable=True)
    companyWebsite = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)

# Crear tablas
Base.metadata.create_all(bind=engine)