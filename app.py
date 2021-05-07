from flask import Flask, request, json, Response
from Utils.utils import ToDict
from Model.user_model import User
from Model.product_model import Product
from database import setup_database
from Controller.product_controller import product_api

app = Flask(__name__)
app.debug = True
app.register_blueprint(product_api)

@app.route('/user')
def get_user():
  return Response('User returned', 201)

@app.route('/user', methods=['POST'])
def create_user(): 
  if not 'username' in request.form:
    return Response('username is missing', 400)
  username = request.form.get('username', '')
  if username == '':
    return Response('{"error-message":"username cannot be empty"}', status=400, mimetype='application/json')

  firstname = request.form.get('firstname', '')
  lastname = request.form.get('lastname', '')

  user = User(username, firstname, lastname)
  s = session()
  s.add(user)
  s.commit()

  return Response('User created', 201)

@app.route('/user', methods=['PATCH'])
def update_user(): 
    return 2+2

@app.route('/user', methods=['DELETE'])
def delete_user(): 
    return 2+2

if __name__ == '__main__':
  setup_database(app)
  app.run('0.0.0.0', port=5000)