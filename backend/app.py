import logging
from flask import Flask
from werkzeug.exceptions import HTTPException
from game_ledger import context, blueprint

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)
_logger.info("Created Logger")

def handle_bad_request(e: HTTPException):
    return e.name, e.code


def create_app():
    app = Flask(__name__)
    app.register_error_handler(HTTPException, handle_bad_request)

    with app.app_context():
        context.init()

    app.register_blueprint(blueprint)
    return app

app = create_app()
_logger.info("Post Create App")