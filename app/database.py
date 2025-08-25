from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Подключение к PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:123Wayther@localhost:5432/postgres"

# Создание движка и сессии
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для зависимости в FastAPI
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
