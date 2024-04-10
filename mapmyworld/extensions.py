
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import getenv
from flask_restful_swagger_3 import Api


ALLOWED_ORIGINS = getenv('ALLOWED_ORIGINS')
SWAGGER_URL = getenv('SWAGGER_URL')

api = Api(title="Map My World", version="1.0",
          description="The contact information for the API. Maps to the contact field of the info object.",
          contact={
              "name": "API Map My World",
              "url": "https://gitlab.com/D4h547/d4h547",
              "email": "support@MapMyWorld.com"
          }, errors={
              'MethodNotAllowed': {
                  'message': 'Method Not Allowed',
                  'status': 405,
              }
          })
db = SQLAlchemy()
ma = Marshmallow()
# cors = CORS(supports_credentials=True, resources={r"/api/v1/*": {"origins": "ALLOWED_ORIGINS"}})
cors = CORS(supports_credentials=True, resources={r"/*": {"origins": "*"}})
