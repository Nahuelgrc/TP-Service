from sqlalchemy import Column, Integer, DateTime, Float
from database import Base
from Utils.utils import ToDict

class Transaction(Base, ToDict):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer)
  product_id = Column(Integer)
  creation_date = Column(DateTime)
  quantity = Column(Integer)
  unit_price = Column(Float)

  def __init__(self, user_id, product_id, creation_date, quantity, unit_price):
    self.user_id = user_id
    self.product_id = product_id
    self.creation_date = creation_date
    self.quantity = quantity
    self.unit_price = unit_price