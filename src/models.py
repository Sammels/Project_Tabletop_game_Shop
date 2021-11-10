from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

""" Дополнительная страница для связи Многие-ко-Многим (Категории - Продукт) """
category_product = db.Table(
    "category_product",
    db.metadata,
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)

poster_product = db.Table(
    "poster_product",
    db.metadata,
    db.Column("poster_id", db.Integer, db.ForeignKey("poster.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)

shots_product = db.Table(
    "shots_product",
    db.metadata,
    db.Column("shots_id", db.Integer, db.ForeignKey("shots.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)

product_cart = db.Table('product_cart',
                     db.metadata,
                     db.Column('productcart_id', db.Integer, db.ForeignKey('productcart.id')),
                     db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'))
                     )


class Category(db.Model):
    """Категории"""

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=60), unique=True)

    def __repr__(self):
        return f"Категория: {self.name}"


class Product(db.Model):
    """Настольная игра"""

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=120), unique=True)
    title = db.Column(db.String(length=240), unique=True)
    price = db.Column(db.Integer())
    category = relationship(
        "Category", secondary=category_product, backref=backref("products", lazy=True)
    )
    description = db.Column(db.Text(), unique=True)
    image_poster = relationship('PosterImage', secondary=poster_product, cascade='all, delete-orphan',
                                single_parent=True,
                                backref=backref('products', lazy=True))
    image_shots = relationship('ShotsImage', secondary=shots_product, cascade='all, delete-orphan', single_parent=True,
                               backref=backref('products', lazy=True, ))
    stock = db.Column(db.Boolean())

    product_cart = relationship('ProductCart', backref='add_product_cart', lazy='dynamic')

    def __repr__(self):
        return f"Наименование игры: {self.name}"


# Работа с пользователем.
class User(db.Model, UserMixin):
    """Пользователи"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(40), index=True)

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


class PosterImage(db.Model):
    __tablename__ = "poster"

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.BLOB, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


class ShotsImage(db.Model):
    __tablename__ = "shots"

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.BLOB, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    total_product = db.Column(db.Integer(), default=0)
    total_price = db.Column(db.Integer(), default=0)
    in_oder = db.Column(db.Boolean(), default=True)
    product = relationship('ProductCart', secondary=product_cart, cascade='all, delete-orphan',
                           single_parent=True,
                           backref=backref('cart', lazy=True))


class ProductCart(db.Model):
    __tablename__ = 'productcart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    product_cart = db.Column(db.Integer, db.ForeignKey('product.id'))
    qty = db.Column(db.Integer(), default=0)

