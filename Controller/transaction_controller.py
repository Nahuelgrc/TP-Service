from flask import Blueprint, Flask, request, json, Response, jsonify
from sqlalchemy.sql.expression import false
from Model.transaction_model import Transaction
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from Utils import utils

transaction_api = Blueprint('transaction_api', __name__)

create_transaction_request = {
  "user_id": fields.Int(required=True, validate=lambda val: val > 0),
  "product_id": fields.Int(required=True,  validate=lambda val: val > 0),
  "creation_date": fields.Str(required=True, validate=validate.Length(min=1)),
  "quantity": fields.Int(required=True, validate=lambda val: val > 0),
  "unit_price": fields.Str(required=True, validate=validate.Length(min=1))
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
  product_id = args["product_id"]
  creation_date = args["creation_date"]
  quantity = args["quantity"]
  unit_price = args["unit_price"]
  
  try:
    transaction = Transaction(
      user_id, 
      product_id, 
      utils.Converter.stringToDatetime(creation_date), 
      quantity, 
      float(unit_price)
      )
    s = get_db_session()
    s.add(transaction)
    s.commit()
    return Response('transaction created', 201)
  except ValueError:
    return Response("incorrect format", 500)
  except:
    return Response("transaction cannot be created", 500)

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