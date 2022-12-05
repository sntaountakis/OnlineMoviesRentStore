import requests
from functools import wraps
import json
from datetime import datetime

class KeyRockAPI():
    def __init__(self) -> None:
        self.admin_token = None
        self.admin_token_expires = datetime.now()
        
    
    def update_admin_token(f):
        def wrapped(self, *args, **kwargs):
            
            admin_values = {
                'name': 'admin@test.com',
                'password': '1234'
            }

            admin_headers = {
                'Content-Type': 'application/json'
            }

            admin = requests.post('http://localhost:3000/v1/auth/tokens', data=json.dumps(admin_values), headers=admin_headers)
            print(admin.headers['X-Subject-Token'])
            self.admin_token = admin.headers['X-Subject-Token']
            self.admin_token_expires = datetime.strptime(admin.json()['token']['expires_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            return f(self, *args, **kwargs)
        return wrapped


    @update_admin_token
    def get_user_token(self, email, password):
        values = {
            'name': email,
            'password': password
        }

        headers = {
            'Content-Type': 'application/json'
        }

        resp = requests.post('http://localhost:3000/v1/auth/tokens', data=json.dumps(values), headers=headers)
        return resp.headers['X-Subject-Token']
        

    @update_admin_token
    def register_user(self, username, email, password):
        values = {
            "user": {
                "username": username,
                "email": email,
                "password": password
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self.admin_token 
        }

        return requests.post('http://localhost:3000/v1/users', data=json.dumps(values), headers=headers)
        
    @update_admin_token
    def get_user_from_token(self, token):
        headers = {
            'X-Auth-token': self.admin_token,
            'X-Subject-token': token
        }
        
        resp = requests.get('http://localhost:3000/v1/auth/tokens', headers=headers)
        return resp.json()