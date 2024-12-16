from base import Base
from albums import Album
from genres import Genre
from users import User
from performers import Performer
from sqlalchemy import create_engine
from sqlalchemy.orm import registry

# Подключение к базе данных PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/audio_db"

engine = create_engine(DATABASE_URL)

# Создание таблицы в базе данных
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    mapper_registry = registry()
    mapper_registry.configure()
    print("Таблица Albums успешно создана.")