from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

Session = sessionmaker()

def get_db_session():
  return Session()

def setup_database(app):
  engine = create_engine('sqlite:///shopdb.sqlite')
  Base.metadata.create_all(engine, checkfirst=True)
  Session.configure(bind=engine)