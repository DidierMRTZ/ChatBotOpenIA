from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from config.Database import engine

# Definir base y modelo
Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'tb_conversations'

    # Columnas basadas en la imagen proporcionada
    ConversationId = Column(Integer, primary_key=True, autoincrement=True)
    CreationTimestamp = Column(DateTime, nullable=True)
    CreatedBy = Column(String(255), nullable=True)
    ModificationTimestamp = Column(DateTime, nullable=True)
    ModifiedBy = Column(String(255), nullable=True)
    CommetCpt = Column(String(255), nullable=True)
    CommetUser = Column(String(255), nullable=True)
    TextCommet = Column(String(500), nullable=True)
    ChatId = Column(Integer, nullable=True)

# Crear tablas
Base.metadata.create_all(engine)
