from flask import Blueprint, Flask, request, json, Response, jsonify
from Model.user_model import User
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound

user_api = Blueprint('user_api', __name__)

create_user_request = {
  "username": fields.Str(required=True, validate=validate.Length(min=1)),
  "firstname": fields.Str(required=True, validate=validate.Length(min=1)),
  "lastname": fields.Str(required=True, validate=validate.Length(min=1))
}

patch_user_request = {
  "username": fields.Str(validate=validate.Length(min=1)),
  "firstname": fields.Str(validate=validate.Length(min=1)),
  "lastname": fields.Str(validate=validate.Length(min=1))
}

# Return validation errors as JSON
@user_api.errorhandler(422)
@user_api.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

@user_api.route('/user')
def list_user():
  s = get_db_session()
  users = s.query(User)
  return Response(json.dumps([u.to_dict() for u in users]), status=200, mimetype='application/json')

@user_api.route('/user/<id>')
def get_user(id):
  s = get_db_session()
  try:
    user = s.query(User).filter_by(id=id).one()
    return Response(json.dumps(user.to_dict()), status=200, mimetype='application/json')
  except NoResultFound:
    return Response("User does not exist", 404)
  return Response('User returned', 201)

@user_api.route('/user', methods=['POST'])
@use_args(create_user_request)
def create_user(args, location="form"):
  user = User(args["username"], args["firstname"], args["lastname"])
  s = get_db_session()
  s.add(user)
  s.commit()
  return Response('User created', 201)

@user_api.route('/user', methods=['PATCH'])
@use_args(patch_user_request)
def update_user(args, location="form"): 
  return 2+2

@user_api.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  s = get_db_session()
  try:
    user = s.query(User).filter_by(id=id).one()
    print("user =>", user)
    s.delete(user)
    s.commit()
    return Response('User deleted', 200)
  except NoResultFound:
    return Response("User does not exist", 404)