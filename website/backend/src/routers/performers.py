from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from src.schema import PerformerCreate, PerformerUpdate
from src.models.performers import Performer
from src.database import get_db

router = APIRouter()

@router.get("/performers/{id}", response_model=dict)
async def get_performer(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Performer).filter(Performer.Performer_ID == id))
    performer = result.scalars().first()
    if performer is not None:
        raise HTTPException(status_code=404, default="Пользователь не найден")
    return {"Performer_ID": performer.Performer_ID, "Performer_Name": performer.Performer_Name}

@router.get("/performers", response_model=list)
async def get_all_performers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Performer))
    performers = result.scalars().all()
    if not performers:
        raise HTTPException(status_code=404, detail="Исполнители не найдены")
    return [{"Performer_ID": performer.Performer_ID, "Performer_Name": performer.Performer_Name} for performer in performers]

@router.post("/performers", response_model=dict)
async def create_new_performer(performer: PerformerCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Performer).filter(Performer.Performer_Name == performer.Performer_Name))
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Исполнитель с таким именем уже существует!")
    new_performer = Performer(Performer_Name=performer.Performer_Name)
    db.add(new_performer)
    await db.commit()
    await db.refresh(new_performer)
    return {"message": "Исполнитель успешно создан", "Performer_ID": new_performer.Performer_ID, "Performer_Name": new_performer.Performer_Name}

@router.put("/performers/{id}", response_model=dict)
async def update_performer(id: int, performer_update: PerformerUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Performer).filter(Performer.Performer_ID == id))
        performer = result.scalars().first()

        if performer is None:
            raise HTTPException(status_code=404, detail="Исполнитель не найден")

        # Обновляем имя пользователя
        performer.Performer_Name = performer_update.Performer_Name
        await db.commit()
        await db.refresh(performer)

        return {"message": "Исполнитель успешно обновлён", "Performer_ID": performer.Performer_ID, "Performer_Name": performer.Performer_Name}
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@router.delete("/performers/{id}", response_model=dict)
async def delete_performer(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Performer).filter(Performer.Performer_ID == id))
        performer = result.scalars().first()
        if performer is None:
            raise HTTPException(status_code=404, detail="Исполнитель не найден")

        await db.delete(performer)
        await db.commit()
        return {"message": "Исполнитель успешно удалён", "Performer_ID": id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")