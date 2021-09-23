from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from db import BDConnector, engine


class Product(BDConnector):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=120))
    title = Column(String(length=240))
    price = Column(Integer())
    image = Column(Integer())
    # categories = ForeignKey
    description = Column(Text())
    stock = Column(Boolean(create_constraint=True))


if __name__ == "__main__":
    BDConnector.metadata.create_all(bind=engine)
