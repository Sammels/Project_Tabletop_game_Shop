from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref

# Попытка в Логин
from flask_login import UserMixin
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import InputRequired, Length, ValidationError

from src.db import BDConnector, engine

""" Дополнительная страница для связи Многие-ко-Многим (Категории - Продукт) """
category_product = Table(
    "category_product",
    BDConnector.metadata,
    Column("category_id", Integer, ForeignKey("category.id")),
    Column("product_id", Integer, ForeignKey("product.id")),
)


class Category(BDConnector):
    """Категории"""

    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=60), unique=True)

    def __repr__(self):
        return f"Категория: {self.name}"


class Product(BDConnector):
    """Настольная игра"""

    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=120), unique=True)
    title = Column(String(length=240), unique=True)
    price = Column(Integer())
    image = Column(Integer())
    category = relationship(
        "Category", secondary=category_product, backref=backref("products", lazy=True)
    )
    description = Column(Text(), unique=True)
    stock = Column(Boolean())

    def __repr__(self):
        return f"Наименование игры: {self.name}"


# Работа с пользователем.
class User(BDConnector, UserMixin):
    """Пользователи"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(40), index=True)

    def set_password(self, password):
        """Хеширование пароля"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        # Проверка. Администратор ли?
        return self.role == "admin" and self.is_active

    def __repr__(self):
        return f"<Пользователь {self.username}, Роль: {self.role}>"


# Создание БД
BDConnector.metadata.create_all(bind=engine)
