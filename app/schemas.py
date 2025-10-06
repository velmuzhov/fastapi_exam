from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, HttpUrl


class BaseCategory(BaseModel):
    """
    Базовая модель для категории
    """

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            description="Название категории (3-50 символов)",
        ),
    ]
    parent_id: Annotated[
        int | None,
        Field(
            default=None,
            description="ID родительской категории, если есть",
        ),
    ]


class CategoryCreate(BaseCategory):
    """
    Модель для создания и обновления категории.
    Используется в POST и PUT запросах.
    """

    ...


class Category(BaseCategory):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """

    id: Annotated[int, Field(description="Уникальный идентификатор категории")]
    is_active: Annotated[bool, Field(description="Активность категории")]

    model_config = ConfigDict(from_attributes=True)


class BaseProduct(BaseModel):
    """
    Базовая модель для товара.
    """

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
            description="Название товара (3-100 символов)",
        ),
    ]
    description: Annotated[
        str,
        Field(
            default=None,
            max_length=500,
            description="Описание товара (до 500 символов)",
        ),
    ]
    price: Annotated[float, Field(gt=0, description="Цена товара (больше 0)")]
    image_url: Annotated[
        HttpUrl,
        Field(
            default=0,
            max_length=200,
            description="URL изображения товара",
        ),
    ]
    stock: Annotated[
        int, Field(ge=0, description="Количество товара на складе (0 или больше)")
    ]
    category_id: Annotated[
        int, Field(description="ID категории, к которой относится товар")
    ]


class ProductCreate(BaseProduct):
    """
    Модель для создания и обновления товара.
    Используется в POST и PUT запросах.
    """

    ...


class Product(BaseProduct):
    """
    Модель для ответа с данными товара.
    Используется в GET-запросах.
    """

    id: Annotated[int, Field(description="Уникальный идентификатор товара")]
    is_active: Annotated[bool, Field(description="Активность товара")]

    model_config = ConfigDict(from_attributes=True)
