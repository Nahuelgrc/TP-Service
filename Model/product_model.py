from sqlalchemy import Column, Integer, String, Float
from database import Base
from Utils.utils import ToDict

class Product(Base, ToDict):
  __tablename__ = 'product'
  id = Column(Integer, primary_key=True)
  name = Column(String)
  description = Column(String)
  imageSrc = Column(String)
  price = Column(Float)

  def __init__(self, name, description, imageSrc, price):
      self.name = name
      self.description = description
      self.imageSrc = imageSrc
      self.price = price