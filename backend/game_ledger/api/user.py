from atexit import register
from multiprocessing import context
from game_ledger.context import Context
from http import HTTPStatus
from datetime import timedelta
from flask import request, make_response, redirect, jsonify
from game_ledger.resources.user import User

_auth_token_name = "gl_auth_token"


@app.route("/user", method="GET")
def user_get():
    pass


# TODO: move this from global to application scope
context = Context()


@app.route("/user/auth", method="POST")
def user_auth_post():
    # check if the content type is application/json
    # then parse the json body
    email = body.get("email", None)
    if email is None:
        raise HTTPStatus.BAD_REQUEST
    register = body.get("register", False)

    if register:
        try:
            User.get_by_email(context.conn, email)
        except HTTPStatus.NOT_FOUND:
            pass
        else:
            raise HTTPStatus.BAD_REQUEST from None

        temp_signin_token = context.token_controller.new_register_token(email)
        context.user_comms.send_register_email(email, temp_signin_token)
        return HTTPStatus.OK

    user = User.get_by_email(context.conn, email)
    auth_token = user.create_auth_token(
        context.conn, timedelta(days=30), request.headers["User-Agent"]
    )
    temp_auth_token = context.token_controller.new_signin_token(auth_token)
    context.user_comms.send_auth_email(email, temp_auth_token)


@app.route("/user/auth", method="GET")
def user_auth_get():
    register = request.args.get("register", False)
    redirect_url = request.args.get("redirect", "/")
    token = request.args.get("token", None)
    if token is None:
        raise HTTPStatus.BAD_REQUEST

    if register:
        email = context.token_controller.use_register_token(token)
        try:
            User.get_by_email(context.conn, email)
        except HTTPStatus.NOT_FOUND:
            pass
        else:
            raise HTTPStatus.BAD_REQUEST from None

        user = User()
        user.name = "Player"
        user.email = email
        user.save(context.conn)
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
    except HTTPStatus.NOT_FOUND:
        return None
    except HTTPStatus.GONE:
        return None


@app.route("/user", method="GET")
def user_get():
    current_user = get_current_user()
    if current_user is None:
        raise HTTPStatus.UNAUTHORIZED
    requested_user_ids = request.args.get("id", current_user.id)
    if type(requested_user_ids) != list:
        requested_user_ids = [requested_user_ids]

    requested_users = [User.get_by_id(id) for id in requested_user_ids]
    response = [
        u.to_dict(u.get_access_level_for_user(current_user)) for u in requested_users
    ]
    return jsonify(response)
