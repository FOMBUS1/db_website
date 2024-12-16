from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from src.schema import AlbumCreate,AlbumUpdate
from src.models.albums import Album
from src.database import get_db

router = APIRouter()

@router.get("/albums", response_model=list)
async def get_all_albums(db: AsyncSession = Depends(get_db)):
    query = (select(Album)
                    .options(joinedload(Album.genre))
                    .options(joinedload(Album.performer))
            )
    
    result = await db.execute(query)
    albums = result.scalars().all()
    if not albums:
        raise HTTPException(status_code=404, detail="Альбомы не найдены")
    return [{
            "Album_ID": album.Album_ID,
            "Album_Title": album.Album_Title,
            "Album_Year": album.Album_Year,
            "Performer_Name": album.performer.Performer_Name,
            "Genre_Title": album.genre.Genre_Title
            } for album in albums]

@router.get("/albums/{id}", response_model=dict)
async def get_all_albums(id: int, db: AsyncSession = Depends(get_db)):
    query = (select(Album)
                    .options(joinedload(Album.genre))
                    .options(joinedload(Album.performer))
                    .where(Album.Album_ID == id)
            )
    
    result = await db.execute(query)
    album = result.scalars().first()
    if not album:
        raise HTTPException(status_code=404, detail="Альбом не найден")
    return {
            "Album_ID": album.Album_ID,
            "Album_Title": album.Album_Title,
            "Album_Year": album.Album_Year,
            "Performer_Name": album.performer.Performer_Name,
            "Genre_Title": album.genre.Genre_Title
            }

@router.post("/albums", response_model=dict)
async def create_new_album(album: AlbumCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Album).filter(Album.Album_Title == album.Album_Title))
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Пользователь с таким именем уже существует!")
    new_album = Album(Album_Title=album.Album_Title, 
                      Album_Year=album.Album_Year, 
                      Performer_FK=album.Performer_FK, 
                      Genre_FK=album.Genre_FK)
    db.add(new_album)
    await db.commit()
    await db.refresh(new_album)
    return {
            "Album_Title": album.Album_Title,
            "Album_Year": album.Album_Year,
            "Performer_FK": album.Performer_FK,
            "Genre_FK": album.Genre_FK
            }

@router.delete("/albums/{id}", response_model=dict)
async def delete_album(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Album).filter(Album.Album_ID == id))
        album = result.scalars().first()
        if album is None:
            raise HTTPException(status_code=404, detail="Альбом не найден")

        await db.delete(album)
        await db.commit()
        return {"message": "Альбом успешно удалён", "Album_ID": id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
    
@router.put("/albums/{id}", response_model=dict)
async def update_album(id: int, album_update: AlbumUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Album).filter(Album.Album_ID == id))
        album = result.scalars().first()

        if album is None:
            raise HTTPException(status_code=404, detail="Альбом не найден")

        album.Album_Title = album_update.Album_Title
        album.Album_Year = album_update.Album_Year
        album.Performer_FK = album_update.Performer_FK
        album.Genre_FK = album_update.Genre_FK
        await db.commit()
        await db.refresh(album)

        return {"message": "Альбом успешно обновлён",
            "Album_Title": album.Album_Title,
            "Album_Year": album.Album_Year,
            "Performer_FK": album.Performer_FK,
            "Genre_FK": album.Genre_FK
            }

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")