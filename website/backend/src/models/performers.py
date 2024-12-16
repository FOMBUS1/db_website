from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapped_column
from typing import List
from src.models.base import Base

# Определение модели Users
class Performer(Base):
    __tablename__ = 'Performers'

    Performer_ID = mapped_column(Integer, primary_key=True, autoincrement=True)
    Performer_Name = mapped_column(String, nullable=False)

    # Связь с альбомами (один ко многим)
    albums = relationship("Album", back_populates="performer")
