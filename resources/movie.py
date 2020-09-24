from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import (
    Response,request
)
from mongoengine.errors import (
    FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
)

from .errors import (
    SchemaValidationError, MovieAlreadyExistsError,
    InternalServerError, UpdatingMovieError, DeletingMovieError, MovieNotExistsError
)
from database.models import Movie, User


class MoviesApi(Resource):
    def get(self):
        movies = Movie.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            # GETTING THE USER
            user = User.objects.get(id=user_id)
            movie = Movie(**body, added_by=user)
            movie.save()

            user.movies.append(movie)
            # user.update(push__movies=movie)
            user.save()

            id = movie.id

            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise MovieAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class MovieApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            movie = Movie.objects.get(id=id, added_by=user_id)
            body = request.get_json()

            movie.update(**body)

            return {'msg': 'Successful update'}, 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            movie = Movie.objects.get(id=id, added_by=user_id)
            movie.delete()

            return {'msg': 'Successful delete'}, 200
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError

    def get(self, id):
        try:
            movie = Movie.objects.get(id=id).to_json()

            return Response(movie, mimetype="application/json", status=200)
        except DoesNotExist:
            raise MovieNotExistsError
        except Exception:
            raise InternalServerError