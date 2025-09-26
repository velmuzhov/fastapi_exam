from sqlalchemy import create_engine, Engine


DATABASE_URL: str = "sqlite:///ecommerce.db"

engine: Engine = create_engine(
    url=DATABASE_URL,
    echo=True,
)
