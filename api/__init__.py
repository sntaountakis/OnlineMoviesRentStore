
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api.keyrock.keyrock import KeyRockAPI
import requests
from os import environ

kr = KeyRockAPI()
db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        POSTGRES_HOST=environ.get('POSTGRES_HOST', 'localhost'),
        POSTGRES_PASSWORD=environ.get('POSTGRES_PASSWORD', '1234'),
        POSTGRES_USER=environ.get('POSTGRES_USER', 'admin'),
        POSTGRES_DATABASE=environ.get('POSTGRES_DATABASE', 'flask_db'),
        SECRET_KEY='totally-secret-key',
        KEYROCK_ID='9759729d-d2cf-417a-88e9-202db4c2eff2',
        KEYROCK_SECRET='f399574b-5c31-4e1e-b4cf-d93e99115686',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{}:{}@{}/{}'.format(app.config['POSTGRES_USER'],
                                                                                       app.config['POSTGRES_PASSWORD'],
                                                                                       app.config['POSTGRES_HOST'],
                                                                                       app.config['POSTGRES_DATABASE'])
    if test_config:
        app.config.from_mapping(test_config)
    
    from . import api
    app.register_blueprint(api.bp)

    db.init_app(app)
    migrate.init_app(app, db)

    keyrock_id = "9759729d-d2cf-417a-88e9-202db4c2eff2"
    keyrock_secret = "f399574b-5c31-4e1e-b4cf-d93e99115686"    

    return app