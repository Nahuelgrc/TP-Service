from flask import Blueprint, Flask, request, json, Response, jsonify
from Model.user_model import User
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_

user_api = Blueprint('user_api', __name__)

login_request = {
  "username": fields.Str(required=True, validate=validate.Length(min=1)),
  "password": fields.Str(required=True, validate=validate.Length(min=1))
}

create_user_request = {
  "username": fields.Str(required=True, validate=validate.Length(min=1)),
  "password": fields.Str(required=True, validate=validate.Length(min=1)),
  "email": fields.Str(required=True, validate=validate.Length(min=1)),
  "firstname": fields.Str(required=True, validate=validate.Length(min=1)),
  "lastname": fields.Str(required=True, validate=validate.Length(min=1))
}

update_password_request = {
  "password": fields.Str(required=True, validate=validate.Length(min=1))
}

update_profile_request = {
  "firstname": fields.Str(required=True, validate=validate.Length(min=1)),
  "lastname": fields.Str(required=True, validate=validate.Length(min=1)),
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

@user_api.route('/login', methods=['POST'])
@use_args(login_request)
def login(args, location="form"):
  username = args["username"]
  password = args["password"]
  s = get_db_session()
  try:
    user = s.query(User).filter(User.username==username, User.password==password).one()
    if user != None:
      return jsonify(
          id=user.id,
          username=user.username,
          email=user.email,
          firstname=user.firstname,
          lastname=user.lastname,
          role=user.role
      )
  except NoResultFound:
    return Response("Unauthorized", 401)

@user_api.route('/user', methods=['POST'])
@use_args(create_user_request)
def create_user(args, location="form"):
  username = args["username"]
  password = args["password"]
  email = args["email"]
  firstname = args["firstname"]
  lastname = args["lastname"]
  role = "user"
  user = User(username, password, email, firstname, lastname, role)
  s = get_db_session()
  s.add(user)
  s.commit()
  return Response('User created', 201)

@user_api.route('/user', methods=['PUT'])
@use_args(update_profile_request)
def update_user(args, location="form"):
  firstname = args["firstname"]
  lastname = args["lastname"]
  username = args["username"]
  password = args["password"]
  email = args["email"]
  s = get_db_session()
  id = args["id"]
  try:
    user = s.query(User).filter_by(id=id).one()
    user.username = username
    user.password = password
    user.email = email
    user.firstname = firstname
    user.lastname = lastname
    s.commit()
    return Response('User updated', 200)
  except NoResultFound:
    return Response("User does not exist", 404)

@user_api.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  s = get_db_session()
  try:
    user = s.query(User).filter_by(id=id).one()
    s.delete(user)
    s.commit()
    return Response('User deleted', 200)
  except NoResultFound:
    return Response("User does not exist", 404)