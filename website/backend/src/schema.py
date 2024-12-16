from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    username: str

class PerformerUpdate(BaseModel):
    Performer_Name: str

class GenreUpdate(BaseModel):
    Genre_Title: str

class AlbumCreate(BaseModel):
    Album_Title: str
    Album_Year: int
    Performer_FK: int
    Genre_FK: int

class PerformerCreate(BaseModel):
    Performer_Name: str

class AlbumUpdate(BaseModel):
    Album_Title: Optional[str] = None
    Album_Year: Optional[int] = None
    Performer_FK: Optional[int] = None
    Genre_FK: Optional[int] = None