from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from config.Database import engine

# Definir base y modelo
Base = declarative_base()

class Gpt(Base):
    __tablename__ = 'tb_gpts'

    # Columnas basadas en la imagen proporcionada
    GptId = Column(Integer, primary_key=True, autoincrement=True)
    CreationTimestamp = Column(DateTime, nullable=False)
    CreatedBy = Column(String(255), nullable=False)
    ModificationTimestamp = Column(DateTime, nullable=False)
    ModifiedBy = Column(String(255), nullable=False)
    AsistentId = Column(String(255), nullable=False)

# Crear tablas
Base.metadata.create_all(engine)
