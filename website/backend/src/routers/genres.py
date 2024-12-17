from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from src.schema import GenreCreate, GenreUpdate
from src.models.tables import Genre
from src.database import get_db

router = APIRouter()

# Асинхронный метод для получения пользователя по ID
@router.get("/genres/{id}", response_model=dict)
async def get_genre(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre).filter(Genre.Genre_ID == id))
    genre = result.scalars().first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    return {"Genre_ID": genre.Genre_ID, "Genre_Title": genre.Genre_Title}

@router.get("/genres", response_model=list)
async def get_all_genres(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre))
    genres = result.scalars().all()
    if not genres:
        raise HTTPException(status_code=404, detail="Жанры не найдены")
    return [{"Genre_ID": genre.Genre_ID, "Genre_Title": genre.Genre_Title} for genre in genres]

@router.delete("/genres/{id}", response_model=dict)
async def delete_genre(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Genre).filter(Genre.Genre_ID == id))
        genre = result.scalars().first()
        if genre is None:
            raise HTTPException(status_code=404, detail="Жанр не найден")

        await db.delete(genre)
        await db.commit()
        return {"message": "Жанр успешно удалён", "Genre_ID": id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
    
@router.put("/genres/{id}", response_model=dict)
async def update_genre(id: int, genre_update: GenreUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Genre).filter(Genre.Genre_ID == id))
        genre = result.scalars().first()

        if genre is None:
            raise HTTPException(status_code=404, detail="Жанр не найден")

        # Обновляем имя пользователя
        genre.Genre_Title = genre_update.Genre_Title
        await db.commit()
        await db.refresh(genre)

        return {"message": "Жанр успешно обновлён", "Genre_ID": genre.Genre_ID, "Genre_Title": genre.Genre_Title}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@router.post("/genres", response_model=dict)
async def create_new_genre(genre: GenreCreate, db: AsyncSession = Depends(get_db)):
    print(genre.Genre_Title)
    result = await db.execute(select(Genre).filter(Genre.Genre_Title == genre.Genre_Title))
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Жанр с таким названием уже существует!")
    new_genre = Genre(Genre_Title=genre.Genre_Title)
    db.add(new_genre)
    await db.commit()
    await db.refresh(new_genre)
    return {"message": "Жанр успешно создан", "Genre_ID": new_genre.Genre_ID, "Genre_Title": new_genre.Genre_Title}

    
