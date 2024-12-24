from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from src.schema import MoodTagCreate, MoodTagUpdate
from src.models.tables import MoodTag
from src.database import get_db

router = APIRouter()

# Асинхронный метод для получения пользователя по ID
@router.get("/moodTags/{id}", response_model=dict)
async def get_moodTag(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MoodTag).filter(MoodTag.MoodTag_ID == id))
    moodTag = result.scalars().first()
    if moodTag is None:
        raise HTTPException(status_code=404, detail="Тег настроения не найден")
    return {"MoodTag_ID": moodTag.MoodTag_ID, "MoodTag_Title": moodTag.MoodTag_Title}

@router.get("/moodTags", response_model=list)
async def get_all_moodTags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MoodTag))
    moodTags = result.scalars().all()
    if not moodTags:
        raise HTTPException(status_code=404, detail="Теги настроения не найдены")
    return [{"MoodTag_ID": moodTag.MoodTag_ID, "MoodTag_Title": moodTag.MoodTag_Title} for moodTag in moodTags]

@router.delete("/moodTags/{id}", response_model=dict)
async def delete_moodTag(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(MoodTag).filter(MoodTag.MoodTag_ID == id))
        moodTag = result.scalars().first()
        if moodTag is None:
            raise HTTPException(status_code=404, detail="Тег настроения не найден")

        await db.delete(moodTag)
        await db.commit()
        return {"message": "Тег настроения успешно удалён", "MoodTag_ID": id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
    
@router.put("/moodTags/{id}", response_model=dict)
async def update_moodTag(id: int, moodTag_update: MoodTagUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(MoodTag).filter(MoodTag.MoodTag_ID == id))
        moodTag = result.scalars().first()

        if moodTag is None:
            raise HTTPException(status_code=404, detail="Тег настроения не найден")

        # Обновляем имя пользователя
        moodTag.MoodTag_Title = moodTag_update.MoodTag_Title
        await db.commit()
        await db.refresh(moodTag)

        return {"message": "Тег настроения успешно обновлён", "MoodTag_ID": moodTag.MoodTag_ID, "MoodTag_Title": moodTag.MoodTag_Title}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@router.post("/moodTags", response_model=dict)
async def create_new_moodTag(moodTag: MoodTagCreate, db: AsyncSession = Depends(get_db)):
    print(moodTag.MoodTag_Title)
    result = await db.execute(select(MoodTag).filter(MoodTag.MoodTag_Title == moodTag.MoodTag_Title))
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Тег настроения с таким названием уже существует!")
    new_moodTag = MoodTag(MoodTag_Title=moodTag.MoodTag_Title)
    db.add(new_moodTag)
    await db.commit()
    await db.refresh(new_moodTag)
    return {"message": "Тег настроения успешно создан", "MoodTag_ID": new_moodTag.MoodTag_ID, "MoodTag_Title": new_moodTag.MoodTag_Title}

    
