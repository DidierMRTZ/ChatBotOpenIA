from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.Database import engine, Base

class Chat(Base):
    __tablename__ = 'tb_chats'
    
    # Campos basados en la imagen proporcionada
    ChatId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    CreationTimestamp = Column(DateTime, nullable=True)
    CreatedBy = Column(String(255), nullable=True)
    ModificationTimestamp = Column(DateTime, nullable=True)
    ModifiedBy = Column(String(255), nullable=True)
    UserId = Column(Integer, nullable=True)
    GptId = Column(Integer, nullable=True)


