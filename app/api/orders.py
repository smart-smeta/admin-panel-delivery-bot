from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import OrderRead, OrderCreate
from app.crud import get_orders, create_order, delete_order
from app.deps import get_db
from app.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=List[OrderRead])
def api_list_orders(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return get_orders(db)

@router.post("/", response_model=OrderRead)
def api_create_order(order: OrderCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return create_order(db, user_id=order.user_id, status=order.status, courier_id=order.courier_id)

@router.delete("/{order_id}", response_model=dict)
def api_delete_order(order_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    deleted = delete_order(db, order_id)
    if not deleted:
        raise HTTPException(404, detail="Order not found")
    return {"ok": True}
