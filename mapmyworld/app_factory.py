from config import app_config
from flask import Flask
from mapmyworld.models import *
from mapmyworld.routes import *

def create_app(env_config):
    app = Flask(__name__)
    app.config.from_object(app_config[env_config])
    app.config["FLASK_ENV"] = env_config
    app_config[env_config].init_app(app)
    return app

