from flask import Blueprint

payment_api_blueprint = Blueprint('payment_api', __name__)

from . import routes
