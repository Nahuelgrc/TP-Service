from flask import Blueprint, Flask, request, json, Response
from Model.product_model import Product
from database import get_db_session

product_api = Blueprint('product_api', __name__)

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

@product_api.route('/products', methods=['POST'])
def create_list_products(): 
  return 2+2

@product_api.route('/products')
def get_list_products(): 
  return 2+2

@product_api.route('/product', methods=['PATCH'])
def update_product(): 
    return 2+2

@product_api.route('/product', methods=['DELETE'])
def delete_product(): 
    return 2+2