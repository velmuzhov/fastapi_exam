from sqlalchemy import create_engine, Engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


DATABASE_URL: str = "sqlite:///ecommerce.db"

engine: Engine = create_engine(
    url=DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(200))
    price: Mapped[float] = mapped_column(nullable=False)
