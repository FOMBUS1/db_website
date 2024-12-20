from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    username: str

class PerformerCreate(BaseModel):
    Performer_Name: str

class PerformerUpdate(BaseModel):
    Performer_Name: str


class GenreCreate(BaseModel):
    Genre_Title: str

class GenreUpdate(BaseModel):
    Genre_Title: str

class MoodTagCreate(BaseModel):
    MoodTag_Title: str

class MoodTagUpdate(BaseModel):
    MoodTag_Title: str

class ActionTagCreate(BaseModel):
    ActionTag_Title: str

class ActionTagUpdate(BaseModel):
    ActionTag_Title: str

class AlbumCreate(BaseModel):
    Album_Title: str
    Album_Year: int
    Performer_FK: int
    Genre_FK: int

class AlbumUpdate(BaseModel):
    Album_ID: int
    Album_Title: str
    Album_Year: int
    Performer_FK: int
    Genre_FK: int

class TrackCreate(BaseModel):
    Track_Title: str
    Album_FK: int
    Playlist_FK: Optional[int] = None
    MoodTag_FK: int
    ActionTag_FK: int
    Duration: int

class TrackUpdate(BaseModel):
    Track_Title: str
    Album_FK: int
    Playlist_FK: Optional[int] = None
    MoodTag_FK: int
    ActionTag_FK: int
    Duration: int