from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from db import BDConnector, engine

""" Дополнительная страница для связи Многие-ко-Многим (Категории - Продукт) """
category_product = Table('category_product',
                         BDConnector.metadata,
                         Column('category_id', Integer, ForeignKey('category.id')),
                         Column('product_id', Integer, ForeignKey('product.id'))
                         )


class Category(BDConnector):
    """ Категории """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=60), unique=True)

    def __repr__(self):
        return f'Категория: {self.name}'


class Product(BDConnector):
    """ Настольная игра"""
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=120), unique=True)
    title = Column(String(length=240), unique=True)
    price = Column(Integer())
    image = Column(Integer())
    category = relationship('Category', secondary=category_product,
                            backref=backref('products', lazy=True))
    description = Column(Text(), unique=True)
    stock = Column(Boolean())

    def __repr__(self):
        return f'Наименование игры: {self.name}'


# Создание БД
BDConnector.metadata.create_all(bind=engine)
