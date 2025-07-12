from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, UserRole
from app.deps import get_db
from app.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list)
def list_users(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return db.query(User).all()

@router.post("/", response_model=dict)
def add_user(user: dict, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    db_user = User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id}

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}
