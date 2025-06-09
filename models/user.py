from sqlalchemy import Column 
from sqlalchemy.sql.sqltypes import Integer, String
from config.Database import engine, Base

class User(Base):
    __tablename__ = 'tb_users'
    userId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String(255), nullable=True)
    lastName = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)

