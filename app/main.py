from fastapi import FastAPI


app = FastAPI(
    title="FastAPI Интернет-магазин",
    version="0.1.0",
)


# Корневой endpoint для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать в API интернет-магазина!"}
