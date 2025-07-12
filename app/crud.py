from app.models import User, UserRole, Product, ProductUnit, Order

# ---- Users ----

def get_users(db):
    return db.query(User).all()

def get_user(db, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db, name: str, tg_id: int = None, role: UserRole = UserRole.user):
    db_user = User(name=name, tg_id=tg_id, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db, user_id: int, **kwargs):
    user = get_user(db, user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user

# ---- Products ----

def get_products(db):
    return db.query(Product).all()

def create_product(db, name, unit, min_qty):
    db_product = Product(name=name, unit=unit, min_qty=min_qty)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db, product_id):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

# ---- Orders ----

def get_orders(db):
    return db.query(Order).all()

def create_order(db, user_id, status="created", courier_id=None):
    db_order = Order(user_id=user_id, status=status, courier_id=courier_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db, order_id):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return order
