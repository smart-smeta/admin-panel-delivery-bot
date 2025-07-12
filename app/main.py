import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.api import users, products, orders, groups, draws
from app.deps import get_db
from app.crud import (
    get_users, create_user, delete_user,
    get_products, create_product, delete_product,
    get_orders, create_order, delete_order
)

load_dotenv()

app = FastAPI(title="Admin Panel")

# Подключаем API-роутеры
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(groups.router, prefix="/api/groups", tags=["groups"])
app.include_router(draws.router, prefix="/api/draws", tags=["draws"])

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request, db=Depends(get_db)):
    return templates.TemplateResponse("users.html", {"request": request, "users": get_users(db)})

@app.post("/users", response_class=RedirectResponse)
def add_user_page(
    request: Request,
    name: str = Form(...),
    tg_id: str = Form(None),
    role: str = Form("user"),
    db=Depends(get_db)
):
    tg_id_val = int(tg_id) if tg_id else None
    create_user(db, name=name, tg_id=tg_id_val, role=role)
    return RedirectResponse(url="/users", status_code=303)

@app.post("/users/delete", response_class=RedirectResponse)
def delete_user_page(
    request: Request,
    id: int = Form(...),
    db=Depends(get_db)
):
    delete_user(db, id)
    return RedirectResponse(url="/users", status_code=303)

@app.get("/products", response_class=HTMLResponse)
def products_page(request: Request, db=Depends(get_db)):
    return templates.TemplateResponse("products.html", {"request": request, "products": get_products(db)})

@app.post("/products", response_class=RedirectResponse)
def add_product_page(
    request: Request,
    name: str = Form(...),
    unit: str = Form(...),
    min_qty: float = Form(1),
    db=Depends(get_db)
):
    create_product(db, name=name, unit=unit, min_qty=min_qty)
    return RedirectResponse(url="/products", status_code=303)

@app.post("/products/delete", response_class=RedirectResponse)
def delete_product_page(
    request: Request,
    id: int = Form(...),
    db=Depends(get_db)
):
    delete_product(db, id)
    return RedirectResponse(url="/products", status_code=303)

@app.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request, db=Depends(get_db)):
    return templates.TemplateResponse("orders.html", {"request": request, "orders": get_orders(db)})

@app.post("/orders", response_class=RedirectResponse)
def add_order_page(
    request: Request,
    user_id: int = Form(...),
    status: str = Form("created"),
    courier_id: str = Form(None),
    db=Depends(get_db)
):
    courier_val = int(courier_id) if courier_id else None
    create_order(db, user_id=user_id, status=status, courier_id=courier_val)
    return RedirectResponse(url="/orders", status_code=303)

@app.post("/orders/delete", response_class=RedirectResponse)
def delete_order_page(
    request: Request,
    id: int = Form(...),
    db=Depends(get_db)
):
    delete_order(db, id)
    return RedirectResponse(url="/orders", status_code=303)
