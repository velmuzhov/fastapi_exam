from collections.abc import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Зависимость для получения сессии базы данных.
    Создает новую сессию для каждого запроса и закрывает ее после обработки.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
