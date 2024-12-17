from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from src.schema import TrackCreate, TrackUpdate
from src.models.tables import Track, Album
from src.database import get_db

router = APIRouter()

@router.get("/tracks", response_model=list)
async def get_all_tracks(db: AsyncSession = Depends(get_db)):
    query = (select(Track)
                    .options(joinedload(Track.album))
                    .options(joinedload(Track.moodTag))
                    .options(joinedload(Track.actionTag)) 
            )
    
    result = await db.execute(query)
    tracks = result.scalars().all()
    if not tracks:
        raise HTTPException(status_code=404, detail="Треки не найдены")
    return [{
            "Track_ID": track.Track_ID,
            "Track_Title": track.Track_Title,
            "Duration": track.Duration,
            "MoodTag_Title": track.moodTag.MoodTag_Title if track.moodTag is not None else None,
            "ActionTag_Title": track.actionTag.ActionTag_Title if track.actionTag is not None else None,
            "Album_Title": track.album.Album_Title if track.album else None
            } for track in tracks]

@router.get("/tracks/{id}", response_model=dict)
async def get_track(id: int, db: AsyncSession = Depends(get_db)):
    query = (select(Track)
                    .options(joinedload(Track.album))
                    .options(joinedload(Track.moodTag))
                    .options(joinedload(Track.actionTag)) 
                    .where(Track.Track_ID == id)
            )
    
    result = await db.execute(query)
    track = result.scalars().first()
    if not track:
        raise HTTPException(status_code=404, detail="Трек не найдены")
    return {
            "Track_ID": track.Track_ID,
            "Track_Title": track.Track_Title,
            "Duration": track.Duration,
            "MoodTag_Title": track.moodTag.MoodTag_Title if track.moodTag is not None else None,
            "ActionTag_Title": track.actionTag.ActionTag_Title if track.actionTag is not None else None,
            "Album_Title": track.album.Album_Title if track.album else None
            }

@router.post("/tracks", response_model="dict")
async def add_new_track(track: TrackCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Track).filter(Track.Track_Title == track.Track_Title and Track.Album_FK == track.Album_FK))
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Трек с таким именем в этом альбоме уже существует!")
    new_track = Track(Track_Title=track.Track_Title, 
                      Album_FK=track.Album_FK,
                      Playlist_FK=track.Playlist_FK if track.Playlist_FK != 0 else None,
                      MoodTag_FK=track.MoodTag_FK,
                      ActionTag_FK=track.ActionTag_FK,
                      Duration=track.Duration)
           
    db.add(new_track)
    await db.commit()
    await db.refresh(new_track)
    return {
            "Track_Title": track.Track_Title,
            "Album_FK": track.Album_FK,
            "Playlist_FK": track.Playlist_FK,
            "MoodTag_FK": track.MoodTag_FK,
            "ActionTag_FK": track.ActionTag_FK,
            "Duration": track.Duration
            }

@router.delete("/tracks/{id}", response_model=dict)
async def delete_track(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Track).filter(Track.Track_ID == id))
        track = result.scalars().first()
        if track is None:
            raise HTTPException(status_code=404, detail="Трек не найден")

        await db.delete(track)
        await db.commit()
        return {"message": "Трек успешно удалён", "Track_ID": id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
    
@router.put("/tracks/{id}", response_model=dict)
async def update_album(id: int, track_update: TrackUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Track).filter(Track.Track_ID == id))
        track = result.scalars().first()

        if track is None:
            raise HTTPException(status_code=404, detail="Трек не найден")

        track.Track_Title = track_update.Track_Title
        track.Album_FK = track_update.Album_FK
        track.Playlist_FK = track_update.Playlist_FK
        track.MoodTag_FK = track_update.MoodTag_FK
        track.ActionTag_FK = track_update.ActionTag_FK
        track.Duration = track_update.Duration
        
        await db.commit()
        await db.refresh(track)

        return {"message": "Трек успешно обновлён",
            "Track_Title": track.Track_Title,
            "Album_FK": track.Track_FK,
            "Playlist_FK": track.Playlist_FK,
            "MoodTag_FK": track.MoodTag_FK,
            "ActionTag_FK": track.ActionTag_FK,
            "Duration": track.Duration
            }

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")