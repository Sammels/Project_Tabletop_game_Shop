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
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from db import BDConnector, engine

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
    login = Column(String(128), nullable=False, unique=True)
    password = Column(String(255), nullable=False)


# Форма регистрации
class RegisterForm(FlaskForm):
    login = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=256)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Регистрация")

    # Проверка имени пользователя
    def validate_username(self, login):
        existing_user_username = User.query.filter_by(login=login.data).first()
        if existing_user_username:
            raise ValidationError("Это имя пользователя уже занято. Исп. другое")


# Форма входа
class LoginForm(FlaskForm):
    login = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=256)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Вход")


# Создание БД
BDConnector.metadata.create_all(bind=engine)
