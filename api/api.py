from flask import Flask, request, jsonify, abort, Blueprint
from api.utils.keyrock_utils import get_admin_token
import requests
import json

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/hello')
def hello():
    return 'Hello, World!'

@bp.route('/register', methods=['POST'])
@get_admin_token()
def register(**kwargs):
    data = request.get_json()

    values = {
        "user": {
            "username": data["username"],
            "email": "test@test.com",
            "password": data["password"]
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-token': kwargs.get('admin_token') 
    }

    user_body = requests.post('http://localhost:3000/v1/users', data=json.dumps(values), headers=headers)
    
    return user_body.json()