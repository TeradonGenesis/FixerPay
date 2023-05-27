from flask import Blueprint

payagent_blueprint = Blueprint('payagent', __name__, url_prefix='/api/v1/payagent')

from . import views