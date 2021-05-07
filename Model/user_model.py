from sqlalchemy import Column, Integer, String
from database import Base
from Utils.utils import ToDict

class User(Base, ToDict):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  username = Column(String)
  firstname = Column(String)
  lastname = Column(String)

  def __init__(self, username, firstname, lastname):
    self.username = username
    self.firstname = firstname
    self.lastname = lastname