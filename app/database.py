from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from app.config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_PORT,
    POSTGRES_HOST
)


# ------- Синхронное подключение к SQLite -------

# DATABASE_URL: str = "sqlite:///ecommerce.db"

# engine: Engine = create_engine(
#     url=DATABASE_URL,
#     echo=True,
# )

# SessionLocal = sessionmaker(bind=engine)


# ------- асинхронное подключение к PostgreSQL -------

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
)

async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass

