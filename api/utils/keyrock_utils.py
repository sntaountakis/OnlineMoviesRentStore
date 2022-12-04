import requests
from functools import wraps
import json

def get_admin_token():
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            
            admin_values = {
                'name': 'admin@test.com',
                'password': '1234'
            }

            admin_headers = {
                'Content-Type': 'application/json'
            }

            admin = requests.post('http://localhost:3000/v1/auth/tokens', data=json.dumps(admin_values), headers=admin_headers)
            print(admin.headers['X-Subject-Token'])
            kwargs['admin_token'] = admin.headers['X-Subject-Token']
            return f(*args, **kwargs)
        return wrapped
    return decorator
