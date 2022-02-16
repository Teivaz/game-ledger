from .user import user_blueprint
from flask.blueprints import Blueprint

blueprint = Blueprint("api", __name__, url_prefix="/api")

blueprint.register_blueprint(user_blueprint, url_prefix="/user")
