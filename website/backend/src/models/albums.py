from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, mapped_column, Mapped

from src.models.base import Base
from src.models.performers import Performer
from src.models.genres import Genre
from typing import List


class Album(Base):
    __tablename__ = 'Albums'

    Album_ID = mapped_column(Integer, primary_key=True, autoincrement=True)
    Album_Title = mapped_column(String, nullable=False)
    Album_Year = mapped_column(Integer, nullable=False)
    Performer_FK = mapped_column(Integer, ForeignKey("Performers.Performer_ID"))
    Genre_FK = mapped_column(Integer, ForeignKey("Genres.Genre_ID"))

    # Связь с исполнителями
    performer = relationship("Performer", back_populates="albums", lazy="selectin")
    # Связь с жанрами (один альбом связан с одним жанром)
    genre = relationship("Genre", back_populates="albums", lazy="selectin")

