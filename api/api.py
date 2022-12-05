from flask import Flask, request, jsonify, abort, Blueprint
from api.utils.keyrock_utils import get_admin_token
from api import kr
import requests
import json

bp = Blueprint('api', __name__, url_prefix='/api')


@kr.require_auth
@bp.route('/hello')
def hello():
    return 'Hello, World!'

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    resp = kr.register_user(data["username"], data["email"], data["password"])

    return resp.json()

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    token = kr.get_user_token(data["email"], data["password"])
    
    return {'token': token}

@bp.route('/user', methods=['GET'])
def user():
    #token = request.headers.get('Authorization').split()[1]
    print("The token is {}".format(token))
    resp = kr.get_user_from_token(token)

    return resp