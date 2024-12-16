from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.models.base import Base

# Определение модели Users
class User(Base):
    __tablename__ = 'Users'

    User_ID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, nullable=False)

