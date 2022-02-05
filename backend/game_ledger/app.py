from flask import Flask
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.errorhandler(HTTPException)
def handle_bad_request(e: HTTPException):
    return e.name, e.code

# or, without the decorator
app.register_error_handler(HTTPException, handle_bad_request)
