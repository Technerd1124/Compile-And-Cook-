from flask import Blueprint
from flask_restx import Api

from src.compile_n_cook.api.endpoints.login import LOGIN_API

AUTH_BLUEPRINT = Blueprint('log', __name__)


API = Api(AUTH_BLUEPRINT)

API.add_namespace(LOGIN_API)
