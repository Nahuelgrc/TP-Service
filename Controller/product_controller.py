from flask import Blueprint, Flask, request, json, Response, jsonify
from sqlalchemy.sql.expression import false
from Model.product_model import Product
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound

product_api = Blueprint('product_api', __name__)

delete_products_request = {
  "ids": fields.Field(required=false)
}

@product_api.route('/product')
def get_product(): 
  s = get_db_session()
  products = s.query(Product)
  print(products)
  return Response(json.dumps([d.to_dict() for d in products]), status=200, mimetype='application/json')

@product_api.route('/product', methods=['POST'])
def create_product():
  if not 'name' in request.form:
    return Response('name is missing', 400)

  name = request.form.get('name', '')
  if name == '':
    return Response('{"error-message":"name cannot be empty"}', status=400, mimetype='application/json')
  image = request.form.get('image', '')
  description = request.form.get('description', '')

  product = Product(name, description, image)

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