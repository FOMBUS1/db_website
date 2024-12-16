from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from src.models.base import Base

class Genre(Base):
    __tablename__ = 'Genres'

    Genre_ID = Column(Integer, primary_key=True, autoincrement=True)
    Genre_Title = Column(String, nullable=False)

    # Связь с альбомами (один жанр может быть у нескольких альбомов)
    albums = relationship("Album", back_populates="genre")

