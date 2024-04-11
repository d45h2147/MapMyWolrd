from mapmyworld.app_factory import create_app
from mapmyworld.app_config import configure_app
import os

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)
configure_app(app)
