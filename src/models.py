from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Table, BLOB, LargeBinary
from sqlalchemy.orm import relationship, backref

from db import BDConnector, engine

""" Дополнительная страница для связи Многие-ко-Многим (Категории - Продукт) """
category_product = Table('category_product',
                         BDConnector.metadata,
                         Column('category_id', Integer, ForeignKey('category.id')),
                         Column('product_id', Integer, ForeignKey('product.id'))
                         )

poster_product = Table('poster_product',
                       BDConnector.metadata,
                       Column('poster_id', Integer, ForeignKey('poster.id')),
                       Column('product_id', Integer, ForeignKey('product.id'))
                       )

shots_product = Table('shots_product',
                      BDConnector.metadata,
                      Column('shots_id', Integer, ForeignKey('shots.id')),
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
    image_poster = relationship('PosterImage', secondary=poster_product,
                                backref=backref('products', lazy=True))
    image_shots = relationship('ShotsImage', secondary=shots_product,
                               backref=backref('products', lazy=True))
    category = relationship('Category', secondary=category_product,
                            backref=backref('products', lazy='joined'))
    description = Column(Text())
    stock = Column(Boolean())

    def __repr__(self):
        return f'Наименование игры: {self.name}'


class PosterImage(BDConnector):
    __tablename__ = 'poster'

    id = Column(Integer, primary_key=True)
    img = Column(BLOB, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    mimetype = Column(Text, nullable=False)


class ShotsImage(BDConnector):
    __tablename__ = 'shots'

    id = Column(Integer, primary_key=True)
    img = Column(BLOB, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    mimetype = Column(Text, nullable=False)


# Создание БД
BDConnector.metadata.create_all(bind=engine)
