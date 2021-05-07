from sqlalchemy import Column, Integer, String
from database import Base
from Utils.utils import ToDict

class Product(Base, ToDict):
  __tablename__ = 'product'
  id = Column(Integer, primary_key=True)
  name = Column(String)
  description = Column(String)
  image = Column(String)

  def __init__(self, name, description, image):
      self.name = name
      self.description = description
      self.image = image