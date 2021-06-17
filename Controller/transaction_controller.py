from flask import Blueprint, Flask, request, json, Response, jsonify
from sqlalchemy.sql.expression import false
from Model.transaction_model import Transaction
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from Utils import utils
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

transaction_api = Blueprint('transaction_api', __name__)

create_transaction_request = {
  "user_id": fields.Int(required=True),
  "cart": fields.Field(required=True)
}

# Return validation errors as JSON
@transaction_api.errorhandler(422)
@transaction_api.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

@transaction_api.route('/transaction')
def list_transaction():
  s = get_db_session()
  transactions = s.query(Transaction)
  return Response(json.dumps([u.to_dict() for u in transactions]), status=200, mimetype='application/json')

@transaction_api.route('/transaction/<id>')
def get_transaction(id):
  s = get_db_session()
  try:
    transaction = s.query(Transaction).filter_by(id=id).one()
    return Response(json.dumps(transaction.to_dict()), status=200, mimetype='application/json')
  except NoResultFound:
    return Response("transaction does not exist", 404)

@transaction_api.route('/transaction/user/<id>')
def get_transactions_by_user(id):
  s = get_db_session()
  try:
    transactions = s.query(Transaction).filter_by(user_id=id)
    return Response(json.dumps([u.to_dict() for u in transactions]), status=200, mimetype='application/json')
  except NoResultFound:
    return Response("transactions do not exist", 404)

@transaction_api.route('/transaction', methods=['POST'])
@use_args(create_transaction_request)
def create_transaction(args, location="form"):
  user_id = args["user_id"]
  cart = args["cart"]
  s = get_db_session()
  try:
    for product in cart:
      print("product =>", product)
      transaction = Transaction(
        user_id, 
        product["id"], 
        datetime.now(), 
        product["quantity"], 
        product["price"])
      print("transaction ==>", transaction)
      s.add(transaction)
    s.commit()
    return Response('transactions created', 201)
  except ValueError:
    return Response("incorrect format", 500)
  except SQLAlchemyError as e:
    reason=str(e)
    print(reason)

@transaction_api.route('/transaction/<id>', methods=['DELETE'])
def delete_transaction(id):
  s = get_db_session()
  try:
    transaction = s.query(Transaction).filter_by(id=id).one()
    s.delete(transaction)
    s.commit()
    return Response('transaction deleted', 200)
  except NoResultFound:
    return Response("transaction does not exist", 404)