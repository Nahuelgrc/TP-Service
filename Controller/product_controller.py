from flask import Blueprint, Flask, request, json, Response, jsonify
from sqlalchemy.sql.expression import false
from Model.product_model import Product
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound

product_api = Blueprint('product_api', __name__)

create_product_request = {
  "name": fields.Str(required=True, validate=validate.Length(min=1)),
  "description": fields.Str(required=True, validate=validate.Length(min=1)),
  "imageSrc": fields.Str(required=True, validate=validate.Length(min=1)),
  "price": fields.Float(required=True)
}

delete_products_request = {
  "ids": fields.Field(required=false)
}

@product_api.route('/product')
def get_product(): 
  s = get_db_session()
  products = s.query(Product)
  return Response(json.dumps([d.to_dict() for d in products]), status=200, mimetype='application/json')

@product_api.route('/product', methods=['POST'])
@use_args(create_product_request)
def create_product(args, location="form"):
  name = args["name"]
  description = args["description"]
  imageSrc = args["imageSrc"]
  price = args["price"]
  product = Product(name, description, imageSrc, price)
  s = get_db_session()
  s.add(product)
  s.commit()
  return Response('Product created', 201)

@product_api.route('/products')
def list_products(): 
  s = get_db_session()
  products = s.query(Product)
  return Response(json.dumps([u.to_dict() for u in products]), status=200, mimetype='application/json')

@product_api.route('/product', methods=['PATCH'])
def update_product(): 
    return 2+2


@product_api.route('/products', methods=['DELETE'])
@use_args(delete_products_request)
def delete_products(args, location="form"):
  ids = args["ids"]
  s = get_db_session()
  try:
    s.query(Product).filter(Product.id.in_(ids)).delete()
    s.commit()
    return Response('Products deleted', 200)
  except NoResultFound:
    return Response("Products do not exist", 404)