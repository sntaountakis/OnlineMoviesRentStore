from flask import Flask, request, jsonify, abort, Blueprint
from api.utils.keyrock_utils import get_admin_token
from marshmallow import fields
from api import kr
import requests
import json

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/hello')
@kr.require_auth
def hello():
    return 'Hello, World!'

register_dict = {'username': fields.Str(required=True),
                'email': fields.Str(required=True),
                'password': fields.Str(required=True)}

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if data.keys() != register_dict.keys():
        error_dict = {"error": {"code": 400,
                                "message": "Invalid arguments in body request",
                                "title": "Bad Request"}}
        return error_dict, 400

    resp = kr.register_user(data["username"], data["email"], data["password"])

    return resp.json(), resp.status_code


login_dict = {'email': fields.Str(required=True),
            'password': fields.Str(required=True)}

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if data.keys() != login_dict.keys():
        error_dict = {"error": {"code": 400,
                                "message": "Invalid arguments in body request",
                                "title": "Bad Request"}}
        return error_dict, 400

    resp = kr.get_user_token(data["email"], data["password"])
    
    return resp.json(), resp.status_code


# For Testing
@bp.route('/user', methods=['GET'])
def user():
    token = request.args.get('token')
    print("The token is {}".format(token))
    resp = kr.get_user_from_token(token)

    return resp