from flask import Blueprint, jsonify

from hobbit_core.flask_hobbit.pagination import PageParams, pagination  # NOQA

from app import models  # NOQA
from app import schemas  # NOQA

bp = Blueprint('ping', __name__)


@bp.route('/ping/', methods=['GET'])
def ping():
    return jsonify({'ping': 'ok'})
