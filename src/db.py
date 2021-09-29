from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///shop.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=engine))

BDConnector = declarative_base()
BDConnector.query = db_session.query_property()