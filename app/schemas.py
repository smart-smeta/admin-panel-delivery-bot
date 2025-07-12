from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

# ---- Users ----

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    courier = "courier"

class UserBase(BaseModel):
    name: str
    tg_id: Optional[int]
    role: UserRole = UserRole.user

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str]
    tg_id: Optional[int]
    role: Optional[UserRole]
    is_active: Optional[bool]

class UserRead(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

# ---- Products ----

class ProductUnit(str, Enum):
    gram = "грамм"
    kg = "килограмм"
    pack = "упаковка"
    item = "шт"
    liter = "литр"

class ProductBase(BaseModel):
    name: str
    unit: ProductUnit
    min_qty: float = 1

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    class Config:
        orm_mode = True

# ---- Orders ----

class OrderBase(BaseModel):
    user_id: int
    status: str = "created"
    courier_id: Optional[int] = None

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    user_id: int
    status: str
    courier_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
