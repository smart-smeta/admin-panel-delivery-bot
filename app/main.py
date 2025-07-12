import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.api import users, products, orders, groups, draws

load_dotenv()

app = FastAPI(title="Admin Panel")

# Подключаем роуты
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(groups.router, prefix="/api/groups", tags=["groups"])
app.include_router(draws.router, prefix="/api/draws", tags=["draws"])

# Подключаем статику и шаблоны (если используем SSR)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
