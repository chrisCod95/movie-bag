from flask import (
    Flask, 
    request, 
    Response
)
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager 
from flask_mail import Mail

from database.db import init_db
from database.models import Movie
from resources.errors import errors

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
mail = Mail(app)

#Imports requiring app and mail
from resources.routes import init_routes

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# app.config['MONGODB_SETTINGS'] = {
#     'host': 'mongodb://localhost/movie-bag'
# }

init_db(app)
init_routes(api)
