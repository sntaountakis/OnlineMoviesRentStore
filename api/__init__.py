
from flask import Flask
import requests

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='totally-secret-key',
        KEYROCK_ID='9759729d-d2cf-417a-88e9-202db4c2eff2',
        KEYROCK_SECRET='f399574b-5c31-4e1e-b4cf-d93e99115686'
    )
    if test_config:
        app.config.from_mapping(test_config)
    
    from . import api
    app.register_blueprint(api.bp)
    
    keyrock_id = "9759729d-d2cf-417a-88e9-202db4c2eff2"
    keyrock_secret = "f399574b-5c31-4e1e-b4cf-d93e99115686"    

    return app