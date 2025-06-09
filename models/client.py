from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String
from config.Database import engine, Base



class Client(Base):
    __tablename__ = 'tb_clients'
    clientId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String(255), nullable=True)
    lastName = Column(String(255), nullable=True)

