from flask import Blueprint

from flask_restful import Resource,Api


api_bp = Blueprint('api', __name__)

api = Api(api_bp)

from . import views

