from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from app.db_depends import get_async_db
from app.models.reviews import Review as ReviewModel
from app.schemas import ReviewCreate, Review as ReviewSchema
from app.models.users import User
from app.models.products import Product
from app.auth import get_current_buyer, check_admin
from app.utils import update_product_rating
from app.routers.products import router as product_router


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

product_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Product not found or inactive",
)


@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов.
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return result.all()


@product_router.get("/{product_id}/reviews", response_model=list[ReviewSchema])
async def get_product_reviews(
    product_id: int, db: AsyncSession = Depends(get_async_db)
):
    """
    Возвращает список активных отзывов товара с данным ID.
    """
    product = await db.scalar(
        select(Product).where(
            Product.id == product_id,
            Product.is_active == True,
        )
    )
    if product is None:
        raise product_not_found
    reviews = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True,
        )
    )

    return reviews


@router.post("/", response_model=ReviewSchema)
async def create_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_buyer),
):
    """
    Создает новый отзыв для существующего товара (только для "buyer")
    """
    product = await db.scalar(
        select(Product).where(
            Product.id == review.product_id,
            Product.is_active == True,
        )
    )
    if product is None:
        raise product_not_found
    already_posted = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.user_id == current_user.id,
            ReviewModel.product_id == product.id,
        )
    )
    if already_posted.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only one review per product",
        )

    review_to_db = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(review_to_db)
    await db.commit()
    await update_product_rating(db, product.id)
    await db.refresh(review_to_db)
    return review_to_db


@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(check_admin),
) -> dict[str, str]:
    """
    Логическое удаление отзыва по его ID (только для роли "admin").
    """
    review = await db.scalar(
        select(ReviewModel)
        .where(
            ReviewModel.id == review_id,
            ReviewModel.is_active == True,
        )
    )
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review doesn't exist or is inactive",
        )
    review.is_active = False
    await db.commit()
    await update_product_rating(db, review.product_id)
    return {"message": "Review deleted"}
