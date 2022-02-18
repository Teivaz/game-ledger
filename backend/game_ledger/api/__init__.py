from .user import user_blueprint
from .data import data_blueprint
from flask.blueprints import Blueprint

blueprint = Blueprint("api", __name__, url_prefix="/api")

blueprint.register_blueprint(user_blueprint)
blueprint.register_blueprint(data_blueprint)
