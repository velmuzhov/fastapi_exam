from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL: str = "sqlite:///ecommerce.db"

engine: Engine = create_engine(
    url=DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(bind=engine)
