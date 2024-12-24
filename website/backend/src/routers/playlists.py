from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from src.schema import PlaylistCreate, PlaylistUpdate
from src.models.tables import Playlist
from src.database import get_db

router = APIRouter()

@router.get("/playlists/{userID}", response_model=list)
async def get_all_playlists(userID: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playlist).where(Playlist.User_FK == userID))
    playlists = result.scalars().all()
    if not playlists:
        raise HTTPException(status_code=404, detail="Плейлисты не найдены")
    return [{"Playlist_ID": playlist.Playlist_ID, "Playlist_Title": playlist.Playlist_Title} for playlist in playlists]

@router.delete("/playlists/{id}", response_model=dict)
async def delete_playlist(id: int,  db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Playlist).filter(Playlist.Playlist_ID == id))
        playlist = result.scalars().first()
        if playlist is None:
            raise HTTPException(status_code=404, detail="Плейлист не найден")

        await db.delete(playlist)
        await db.commit()
        return {"message": "Плейлист успешно удалён", "Playlist_ID": id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
    
@router.put("/playlists/{id}", response_model=dict)
async def update_playlist(id: int, playlist_update: PlaylistUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Playlist).filter(Playlist.Playlist_ID == id))
        playlist = result.scalars().first()

        if playlist is None:
            raise HTTPException(status_code=404, detail="Плейлист не найден")

        # Обновляем имя пользователя
        playlist.Playlist_Title = playlist_update.Playlist_Title
        await db.commit()
        await db.refresh(playlist)

        return {"message": "Плейлист успешно обновлён", "Playlist_ID": playlist.Playlist_ID, "Playlist_Title": playlist.Playlist_Title}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@router.post("/playlists", response_model=dict)
async def add_new_playlist(playlist: PlaylistCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playlist).filter(Playlist.Playlist_Title == playlist.Playlist_Title))
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Плейлист с таким именем уже существует!")
    new_playlist= Playlist(Playlist_Title=playlist.Playlist_Title, User_FK=playlist.User_FK)
    db.add(new_playlist)
    await db.commit()
    await db.refresh(new_playlist)
    return {"message": "Плейлист успешно создан", "Playlist_Title": playlist.Playlist_Title}