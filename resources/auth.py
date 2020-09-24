##### IMPORTS #####
# THIRD PARTY
from flask import (
    request, Response,jsonify
)
from mongoengine.errors import (
    FieldDoesNotExist, NotUniqueError, DoesNotExist
)
from flask_restful import Resource
from flask_jwt_extended import create_access_token
import datetime

# MADE BY ME
from .errors import (
    SchemaValidationError, InternalServerError, EmailAlreadyExistsError, UnauthorizedError
)
from database.models import User

class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            
            user.hash_password()
            user.save()
            
            id = user.id
            
            return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError
    
class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
        
            user = User.objects.get(email=body['email'])
            authorized = user.check_password(body.get('password'))
            
            if not authorized: 
                return {'error': 'Email or password invalid'}, 401
            
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(
                identity=str(user.id), 
                expires_delta=expires
            )
            
            return {'token': access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except FieldDoesNotExist:
            raise SchemaValidationError
        except Exception:
            raise InternalServerError
        
        
