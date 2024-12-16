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