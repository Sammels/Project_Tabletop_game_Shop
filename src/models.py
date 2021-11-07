from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Table,
    BLOB,
)
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db import BDConnector, engine

""" Дополнительная страница для связи Многие-ко-Многим (Категории - Продукт) """
category_product = Table(
    "category_product",
    BDConnector.metadata,
    Column("category_id", Integer, ForeignKey("category.id")),
    Column("product_id", Integer, ForeignKey("product.id")),
)

poster_product = Table(
    "poster_product",
    BDConnector.metadata,
    Column("poster_id", Integer, ForeignKey("poster.id")),
    Column("product_id", Integer, ForeignKey("product.id")),
)

shots_product = Table(
    "shots_product",
    BDConnector.metadata,
    Column("shots_id", Integer, ForeignKey("shots.id")),
    Column("product_id", Integer, ForeignKey("product.id")),
)

product_cart = Table('product_cart',
                     BDConnector.metadata,
                     Column('product_id', Integer, ForeignKey('product.id')),
                     Column('cart_id', Integer, ForeignKey('cart.id'))
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
    image_poster = relationship('PosterImage', secondary=poster_product, cascade='all, delete-orphan',
                                single_parent=True,
                                backref=backref('products', lazy=True))
    image_shots = relationship('ShotsImage', secondary=shots_product, cascade='all, delete-orphan', single_parent=True,
                               backref=backref('products', lazy=True, ))
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
    cart = relationship('Cart', backref='user')

    def set_password(self, password):
        """Хеширование пароля"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password, password)

    def is_admin(self):
        # Проверка. Администратор ли?
        return self.role == "admin" and self.is_active

    def __repr__(self):
        return f"<Пользователь {self.username}, Роль: {self.role}>"


class PosterImage(BDConnector):
    __tablename__ = "poster"

    id = Column(Integer, primary_key=True)
    img = Column(BLOB, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    mimetype = Column(Text, nullable=False)


class ShotsImage(BDConnector):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True)
    img = Column(BLOB, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    mimetype = Column(Text, nullable=False)


class Cart(BDConnector):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product = relationship('Product', secondary=product_cart, backref=backref('cart', lazy=True))
    total_product = Column(Integer(), default=0)
    total_price = Column(Integer(), default=0)
    in_oder = Column(Boolean(), default=True)
    for_anonymous_user = Column(Boolean(), default=True)


# Создание БД
BDConnector.metadata.create_all(bind=engine)
