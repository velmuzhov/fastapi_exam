# Интернет-магазин на FastAPI

## Разработка системы отзывов о товарах

Файлы, связанне с реализацией отзывов:

- `app/models/reviews.py` - модель SQLAlchemy. Ограничения на диапазон оценки заданы в `__table_args__`
- `app/schemas.py` - добавлены модели `BaseReview` и ее наследники `ReviewCreate` и `Review`
- `app/routers/reviews.py` - конечные точки, связанные с отзывами. Для реализации одного из эндпоинтов импортирован `app.routers.products.router` для соответствия маршрутам, данным в задании.
- `app/utils.py` - сюда вынесена функция `update_product_rating()`
