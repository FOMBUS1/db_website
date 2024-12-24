from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import and_

from src.schema import AddTrack, DeleteTrack
from src.models.tables import PlaylistTrack, Track, Album, MoodTag, ActionTag
from src.database import get_db

router = APIRouter()

@router.post("/playlist", response_model=dict)
async def add_new_track(playlist: AddTrack, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PlaylistTrack).filter(
            and_(
                PlaylistTrack.Playlist_ID == playlist.Playlist_ID,
                PlaylistTrack.Track_ID == playlist.Track_ID
            )
        )
    )
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Этот трек уже добавлен в этот плейлист!")
    new_playlist= PlaylistTrack(Playlist_ID=playlist.Playlist_ID, Track_ID=playlist.Track_ID)
    db.add(new_playlist)
    await db.commit()
    await db.refresh(new_playlist)
    return {"message": "Трек успешно добавлен в этот плейлист"}

@router.get("/playlist/{id}", response_model=list)
async def get_playlist_tracks(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PlaylistTrack, Track, Album, MoodTag, ActionTag)
                              .join(Track, PlaylistTrack.Track_ID == Track.Track_ID)
                              .join(Album, Track.Album_FK == Album.Album_ID)
                              .join(MoodTag, Track.MoodTag_FK == MoodTag.MoodTag_ID)
                              .join(ActionTag, Track.ActionTag_FK == ActionTag.ActionTag_ID)
                              .filter(PlaylistTrack.Playlist_ID == id)
                            )


    tracks = result.fetchall()
    if (len(tracks) == 0):
        print("Something went wrong!")
        return [{"success": "false"}]

    return [{"Playlist_ID": playlist.Playlist_ID,
             "Track_ID": playlist.Track_ID,
             "Track_Title": track.Track_Title,
             "Album_Title": album.Album_Title,
             "MoodTag_Title": moodTag.MoodTag_Title,
             "ActionTag_Title": actionTag.ActionTag_Title} for playlist, track, album, moodTag, actionTag in tracks]

@router.delete("/playlist")
async def delete_track(playlist: DeleteTrack, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(PlaylistTrack)
                                  .filter(
                                      and_(PlaylistTrack.Playlist_ID == playlist.Playlist_ID,
                                           PlaylistTrack.Track_ID == playlist.Track_ID)
                                        )
                                )
        playlist = result.scalars().first()
        if playlist is None:
            raise HTTPException(status_code=404, detail="Трек не найден в этом плейлисте")

        await db.delete(playlist)
        await db.commit()
        return {"message": "Трек успешно удалён из этого плейлиста", "Playlist_ID": playlist.Playlist_ID, "Track_ID": playlist.Track_ID}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")