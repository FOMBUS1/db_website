from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from src.schema import ActionTagCreate, ActionTagUpdate
from src.models.tables import ActionTag
from src.database import get_db

router = APIRouter()

# Асинхронный метод для получения пользователя по ID
@router.get("/actionTags/{id}", response_model=dict)
async def get_actionTag(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ActionTag).filter(ActionTag.ActionTag_ID == id))
    actionTag = result.scalars().first()
    if actionTag is None:
        raise HTTPException(status_code=404, detail="Тег действия не найден")
    return {"ActionTag_ID": actionTag.ActionTag_ID, "ActionTag_Title": actionTag.ActionTag_Title}

@router.get("/actionTags", response_model=list)
async def get_all_actionTags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ActionTag))
    actionTags = result.scalars().all()
    if not actionTags:
        raise HTTPException(status_code=404, detail="Теги действия не найдены")
    return [{"ActionTag_ID": actionTag.ActionTag_ID, "ActionTag_Title": actionTag.ActionTag_Title} for actionTag in actionTags]

@router.delete("/actionTags/{id}", response_model=dict)
async def delete_actionTag(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(ActionTag).filter(ActionTag.ActionTag_ID == id))
        actionTag = result.scalars().first()
        if actionTag is None:
            raise HTTPException(status_code=404, detail="Тег действия не найден")

        await db.delete(actionTag)
        await db.commit()
        return {"message": "Тег действия успешно удалён", "ActionTag_ID": id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
    
@router.put("/actionTags/{id}", response_model=dict)
async def update_actionTag(id: int, actionTag_update: ActionTagUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(ActionTag).filter(ActionTag.ActionTag_ID == id))
        actionTag = result.scalars().first()

        if actionTag is None:
            raise HTTPException(status_code=404, detail="Тег действия не найден")

        # Обновляем имя пользователя
        actionTag.ActionTag_Title = actionTag_update.ActionTag_Title
        await db.commit()
        await db.refresh(actionTag)

        return {"message": "Тег действия успешно обновлён", "ActionTag_ID": actionTag.ActionTag_ID, "ActionTag_Title": actionTag.ActionTag_Title}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@router.post("/actionTags", response_model=dict)
async def create_new_actionTag(actionTag: ActionTagCreate, db: AsyncSession = Depends(get_db)):
    print(actionTag.ActionTag_Title)
    result = await db.execute(select(ActionTag).filter(ActionTag.ActionTag_Title == actionTag.ActionTag_Title))
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Тег действия с таким названием уже существует!")
    new_actionTag = ActionTag(ActionTag_Title=actionTag.ActionTag_Title)
    db.add(new_actionTag)
    await db.commit()
    await db.refresh(new_actionTag)
    return {"message": "Тег действия успешно создан", "ActionTag_ID": new_actionTag.ActionTag_ID, "ActionTag_Title": new_actionTag.ActionTag_Title}

    
