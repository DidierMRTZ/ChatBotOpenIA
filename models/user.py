from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config.Database import engine

# Definir base y modelo
Base = declarative_base()

class User(Base):
    __tablename__ = 'tb_users'
    userId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String(255), nullable=True)
    lastName = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)

# Crear tablas
Base.metadata.create_all(engine)