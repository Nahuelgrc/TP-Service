from flask import Flask, request, json, Response
from Utils.utils import ToDict
from Model.user_model import User
from Model.product_model import Product
from database import setup_database
from Controller.product_controller import product_api
from Controller.user_controller import user_api

app = Flask(__name__)
app.debug = True
app.register_blueprint(product_api)
app.register_blueprint(user_api)

if __name__ == '__main__':
  setup_database(app)
  app.run('0.0.0.0', port=5000)