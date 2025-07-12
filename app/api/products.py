from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import ProductRead, ProductCreate
from app.crud import get_products, create_product, delete_product
from app.deps import get_db
from app.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=List[ProductRead])
def api_list_products(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return get_products(db)

@router.post("/", response_model=ProductRead)
def api_create_product(product: ProductCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return create_product(db, name=product.name, unit=product.unit, min_qty=product.min_qty)

@router.delete("/{product_id}", response_model=dict)
def api_delete_product(product_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(404, detail="Product not found")
    return {"ok": True}
