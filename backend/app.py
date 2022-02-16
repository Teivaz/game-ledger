from flask import Flask
from werkzeug.exceptions import HTTPException
from game_ledger import context, blueprint


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
