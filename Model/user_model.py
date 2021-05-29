from sqlalchemy import Column, Integer, String
from database import Base
from Utils.utils import ToDict

class User(Base, ToDict):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  username = Column(String)
  password = Column(String)
  email = Column(String)
  firstname = Column(String)
  lastname = Column(String)
  role = Column(String)  

  def __init__(self, username, password, email, firstname, lastname, role):
    self.username = username
    self.password = password
    self.email = email
    self.firstname = firstname
    self.lastname = lastname
    self.role = role