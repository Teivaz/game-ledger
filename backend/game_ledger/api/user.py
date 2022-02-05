from multiprocessing import context
from game_ledger.context import Context
from game_ledger.app import app
from werkzeug.exceptions import *
from datetime import timedelta
from flask import request, make_response, redirect, jsonify
from game_ledger.resources.user import User

_auth_token_name = "gl_auth_token"


# TODO: move this from global to application scope
context = Context()


@app.route("/api/user/auth/", methods=["POST", "GET"])
def cmon_flask_i_want_different_handlers_for_methods():
    if request.method == "GET":
        return user_auth_get()
    if request.method == "POST":
        return user_auth_post()
    else:
        raise MethodNotAllowed()


def user_auth_post():
    body = request.get_json()
    if body is None:
        raise BadRequest()
    email = body.get("email", None)
    if email is None:
        raise BadRequest()
    register = body.get("register", False)

    if register:
        try:
            User.get_by_email(context.conn, email)
        except NotFound:
            pass
        else:
            raise BadRequest() from None

        temp_signin_token = context.token_controller.new_register_token(email)
        context.user_comms.send_register_email(email, temp_signin_token)
        return ""

    user = User.get_by_email(context.conn, email)
    auth_token = user.create_auth_token(
        context.conn, timedelta(days=30), request.headers["User-Agent"]
    )
    temp_auth_token = context.token_controller.new_signin_token(auth_token)
    context.user_comms.send_auth_email(email, temp_auth_token)
    return ""


def user_auth_get():
    register = "register" in request.args
    redirect_url = request.args.get("redirect", "/")
    token = request.args.get("token", None)
    if token is None:
        raise BadRequest()

    if register:
        email = context.token_controller.use_register_token(token)
        try:
            User.get_by_email(context.conn, email)
        except NotFound:
            pass
        else:
            raise BadRequest() from None

        user = User.create(context.conn, name="Player", email=email)
        auth_token = user.create_auth_token(
            context.conn, timedelta(days=30), request.headers["User-Agent"]
        )

    else:
        auth_token = context.token_controller.use_signin_token(token)

    response = make_response(redirect(redirect_url))
    response.set_cookie(_auth_token_name, auth_token)
    return response


def get_current_user():
    token = request.cookies.get(_auth_token_name)
    if token is None:
        return None
    try:
        return User.auth_by_token(context.conn, token)
    except NotFound:
        return None
    except Gone:
        return None


@app.route("/api/user/", methods=["GET", "POST", "DELETE"])
def cmon_flask_i_want_different_handlers_for_methods_2():
    if request.method == "GET":
        return user_get()
    if request.method == "POST":
        return user_post()
    if request.method == "PATCH":
        return user_patch()
    if request.method == "DELETE":
        return user_delete()
    else:
        return MethodNotAllowed()


def user_get():
    current_user = get_current_user()
    if current_user is None:
        raise Unauthorized()
    requested_user_ids = request.args.getlist("id")
    if not requested_user_ids:
        requested_user_ids = [current_user.id]

    requested_users = [User.get_by_id(context.conn, id) for id in requested_user_ids]
    response = [
        u.to_dict(u.get_access_level_for_user(current_user)) for u in requested_users
    ]
    return jsonify(response)

def user_post():
    pass

def user_patch():
    pass

def user_delete():
    pass

