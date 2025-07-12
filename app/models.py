
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    courier = "courier"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, nullable=True)  # может быть None для ручного добавления
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    is_active = Column(Boolean, default=True)

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

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="created")
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # Можно добавить: items, total, created_at и др.

class BroadcastGroup(Base):
    __tablename__ = "broadcast_groups"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    tg_group_id = Column(String)

class Draw(Base):
    __tablename__ = "draws"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    condition = Column(String)
    winners = Column(String)  # можно хранить как JSON-строку
    status = Column(String, default="pending")
