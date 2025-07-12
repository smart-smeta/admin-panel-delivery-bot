import enum
from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# ---- Users ----
class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    courier = "courier"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, nullable=True)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    is_active = Column(Boolean, default=True)

# ---- Products ----
class ProductUnit(str, enum.Enum):
    gram = "грамм"
    kg = "килограмм"
    pack = "упаковка"
    item = "шт"
    liter = "литр"

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    unit = Column(Enum(ProductUnit), nullable=False)
    min_qty = Column(Float, default=1)

# ---- Orders ----
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="created")
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
