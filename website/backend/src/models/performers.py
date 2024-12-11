from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Базовый класс для моделей
Base = declarative_base()

# Определение модели Users
class Performer(Base):
    __tablename__ = 'Performers'

    Performer_ID = Column(Integer, primary_key=True, autoincrement=True)
    Performer_Name = Column(String, nullable=False)

# Подключение к базе данных PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/audio_db"

engine = create_engine(DATABASE_URL)

# Создание таблицы в базе данных
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("Таблица Performers успешно создана.")
