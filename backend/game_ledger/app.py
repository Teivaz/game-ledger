from flask import Flask
from werkzeug.exceptions import HTTPException
from game_ledger.context import Context
from game_ledger.api.user import UserApi, UserSignInApi, UserRegisterApi

app = Flask(__name__)

app.errorhandler(HTTPException)
def handle_bad_request(e: HTTPException):
    return e.name, e.code

# or, without the decorator
app.register_error_handler(HTTPException, handle_bad_request)

ctx = Context()

app.add_url_rule('/api/user/', view_func=UserApi.as_view('user', context=ctx))
app.add_url_rule('/api/user/signin/', view_func=UserSignInApi.as_view('user_sign_in', context=ctx))
app.add_url_rule('/api/user/register/', view_func=UserRegisterApi.as_view('user_register', context=ctx))

