from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    func,
    Integer,
    Text,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


if TYPE_CHECKING:
    from app.models.users import User
    from app.models.products import Product


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(column="products.id", ondelete="CASCADE"),
        nullable=False,
    )
    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    comment_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        server_default=func.now(),
    )
    grade: Mapped[int] = mapped_column(
        Integer,
        # CheckConstraint("grade >= 1 AND grade <=5"),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="reviews",
    )

    __table_args__ = (
        CheckConstraint("grade >= 1 AND grade <= 5", name="grade_check"),
    )