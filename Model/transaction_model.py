from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship,backref
from database import Base
from Utils.utils import ToDict

class Transaction(Base, ToDict):
  __tablename__ = 'transaction'
  id = Column(Integer, primary_key=True)
  product_id = Column(Integer, ForeignKey('product.id'))
  user_id = Column(Integer, ForeignKey('user.id'))
  creation_date = Column(DateTime)
  quantity = Column(Integer)
  unit_price = Column(Float)

  product = relationship(
    "Product",
    backref=backref('transaction', uselist=True, cascade='delete,all')
  )
  user = relationship(
    "User",
    backref=backref('transaction', uselist=True, cascade='delete,all')
  )


  def __init__(self, user_id, product_id, creation_date, quantity, unit_price):
    self.user_id = user_id
    self.product_id = product_id
    self.creation_date = creation_date
    self.quantity = quantity
    self.unit_price = unit_price