from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from src.schema import UserUpdate
from src.models.users import User
from src.database import get_db

router = APIRouter()

# Асинхронный метод для получения пользователя по ID
@router.get("/users/{id}", response_model=dict)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.User_ID == id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"User_ID": user.User_ID, "Username": user.Username}

@router.get("/users/", response_model=list)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="Пользователи не найдены")
    return [{"User_ID": user.User_ID, "Username": user.Username} for user in users]

@router.delete("/users/{id}", response_model=dict)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).filter(User.User_ID == id))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        await db.delete(user)
        await db.commit()
        return {"message": "Пользователь успешно удалён", "User_ID": id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
    
@router.put("/users/{id}", response_model=dict)
async def update_user(id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).filter(User.User_ID == id))
        user = result.scalars().first()

        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Обновляем имя пользователя
        user.Username = user_update.username
        await db.commit()
        await db.refresh(user)

        return {"message": "Пользователь успешно обновлён", "User_ID": user.User_ID, "Username": user.Username}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Асинхронный метод для создания нового пользователя
@router.post("/users/", response_model=dict)
async def create_new_user(username: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.Username == username))
    if (len(result.scalars().all()) > 0):
        raise HTTPException(status_code=403, detail="Пользователь с таким именем уже существует!")
    new_user = User(Username=username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "Пользователь успешно создан", "User_ID": new_user.User_ID, "Username": new_user.Username}

    
