from .movie import (
    MoviesApi, 
    MovieApi
)
from .auth import (
    SignupApi, 
    LoginApi
)
from .reset_password import (
    ForgotPassword,
    ResetPassword
)

def init_routes(api):
    """
    MOVIES RESOURCE ROUTES
    """
    api.add_resource(MoviesApi, '/api/movies')
    api.add_resource(MovieApi, '/api/movies/<id>')
    
    """
    USER AUTH ROUTES
    """
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    
    """
    RESET PASSWORD ROUTES
    """
    api.add_resource(ForgotPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/api/auth/reset')