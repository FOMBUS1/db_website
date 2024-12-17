from src.models.base import Base

from src.models.tables import *

from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship

# Подключение к базе данных PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/audio_db"

engine = create_engine(DATABASE_URL, echo=True)

# Создание таблицы в базе данных
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    mapper_registry = registry()
    mapper_registry.configure()
    print("Все таблицы успешно созданы.")