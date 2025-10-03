from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.categories import Category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False) # переделал на другой тип
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    category_id: Mapped[int] = mapped_column(ForeignKey(column="categories.id", ondelete="CASCADE"), nullable=False) 

    category: Mapped["Category"] = relationship("Category", back_populates="products")
