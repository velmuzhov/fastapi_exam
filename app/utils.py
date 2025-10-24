from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.reviews import Review
from app.models.products import Product


async def update_product_rating(db: AsyncSession, product_id: int) -> None:
    result = await db.execute(
        select(func.avg(Review.grade)).where(
            Review.product_id == product_id,
            Review.is_active == True,
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    product.rating = avg_rating
    await db.commit()
