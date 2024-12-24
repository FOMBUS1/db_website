from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapped_column
from src.models.base import Base

class User(Base):
    __tablename__ = 'Users'

    User_ID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, nullable=False)

    playlists = relationship("Playlist", back_populates="user")

class Genre(Base):
    __tablename__ = 'Genres'

    Genre_ID = Column(Integer, primary_key=True, autoincrement=True)
    Genre_Title = Column(String, nullable=False)

    albums = relationship("Album", back_populates="genre")

class Album(Base):
    __tablename__ = 'Albums'

    Album_ID = mapped_column(Integer, primary_key=True, autoincrement=True)
    Album_Title = mapped_column(String, nullable=False)
    Album_Year = mapped_column(Integer, nullable=False)
    Performer_FK = mapped_column(Integer, ForeignKey("Performers.Performer_ID"))
    Genre_FK = mapped_column(Integer, ForeignKey("Genres.Genre_ID"))

    performer = relationship("Performer", back_populates="albums", lazy="selectin")
    genre = relationship("Genre", back_populates="albums", lazy="selectin")
    tracks = relationship("Track", back_populates="album")

class Performer(Base):
    __tablename__ = 'Performers'

    Performer_ID = mapped_column(Integer, primary_key=True, autoincrement=True)
    Performer_Name = mapped_column(String, nullable=False)

    albums = relationship("Album", back_populates="performer")

class ActionTag(Base):
    __tablename__ = 'ActionTags'

    ActionTag_ID = Column(Integer, primary_key=True, autoincrement=True)
    ActionTag_Title = Column(String, nullable=False)

    tracks = relationship("Track", back_populates="actionTag")

class MoodTag(Base):
    __tablename__ = 'MoodTags'

    MoodTag_ID = Column(Integer, primary_key=True, autoincrement=True)
    MoodTag_Title = Column(String, nullable=False)

    tracks = relationship("Track", back_populates="moodTag")

class PlaylistTrack(Base):
    __tablename__ = 'playlist_track'

    Playlist_ID = Column(Integer, ForeignKey('Playlists.Playlist_ID'), primary_key=True)
    Track_ID = Column(Integer, ForeignKey('Tracks.Track_ID'), primary_key=True)


class Track(Base):
    __tablename__ = 'Tracks'

    Track_ID = mapped_column(Integer, primary_key=True, autoincrement=True)
    Track_Title = mapped_column(String, nullable=False)
    Album_FK = mapped_column(Integer, ForeignKey("Albums.Album_ID"))
    MoodTag_FK = mapped_column(Integer, ForeignKey("MoodTags.MoodTag_ID"))
    ActionTag_FK = mapped_column(Integer, ForeignKey("ActionTags.ActionTag_ID"))
    Duration = mapped_column(Integer, nullable=False)

    playlists = relationship("Playlist", secondary="playlist_track", back_populates="tracks", lazy="selectin")
    actionTag = relationship("ActionTag", back_populates="tracks", lazy="selectin")
    moodTag = relationship("MoodTag", back_populates="tracks", lazy="selectin")
    album = relationship("Album", back_populates="tracks")


class Playlist(Base):
    __tablename__ = 'Playlists'

    Playlist_ID = mapped_column(Integer, primary_key=True, autoincrement=True)
    Playlist_Title = mapped_column(String, nullable=False)
    User_FK = mapped_column(Integer, ForeignKey("Users.User_ID"))
    
    user = relationship("User", back_populates="playlists", lazy="selectin")
    tracks = relationship("Track", secondary="playlist_track", back_populates="playlists", lazy="selectin")
