from game_ledger import context
from werkzeug.exceptions import *
from datetime import timedelta
from flask import Blueprint, request, redirect, jsonify
from flask.views import MethodView
from game_ledger.resources.user import User
import flask


def is_production():
    return flask.current_app.config["ENV"] == "production"


class UserApi(MethodView):
    def get(self):
        current_user = context.get_current_user()
        if current_user is None:
            raise Unauthorized()
        requested_user_ids = request.args.getlist("id")
        if not requested_user_ids:
            requested_user_ids = [current_user.id]

        requested_users = [
            User.get_by_id(context.get_db_connection(), id) for id in requested_user_ids
        ]
        response = [
            u.to_dict(u.get_access_level_for_user(current_user))
            for u in requested_users
        ]
        return jsonify(response)

    def post(self):
        pass

    def patch(self):
        current_user = context.get_current_user()
        if current_user is None:
            raise Unauthorized()
        requested_user_id = request.args.get("id")
        if requested_user_id != current_user.id:
            raise Unauthorized()
        body = request.get_json()
        if body is None:
            raise BadRequest()
        current_user.update_from_dict(body)
        current_user.save(context.get_db_connection())
        return ""

    def delete(self):
        current_user = context.get_current_user()
        if current_user is None:
            raise Unauthorized()
        requested_user_id = request.args.get("id")
        if requested_user_id != current_user.id:
            raise Unauthorized()
        body = request.get_json()
        if body is None:
            raise BadRequest()
        requested_user_id = body.get("id", current_user.id)
        if requested_user_id != current_user.id:
            raise Unauthorized()
        current_user.delete(context.get_db_connection())
        return ""


class UserRegisterApi(MethodView):
    def post(self):
        body = request.get_json()
        if body is None:
            raise BadRequest()
        email = body.get("email", None)
        if email is None:
            raise BadRequest()
        try:
            User.get_by_email(context.get_db_connection(), email)
        except NotFound:
            pass
        else:
            raise BadRequest() from None

        temp_register_token = context.get_token_controller().new_register_token(body)
        context.send_register_email(email, temp_register_token)
        return ""

    def get(self):
        redirect_url = request.args.get("redirect", "/")
        token = request.args.get("token", None)
        if token is None:
            raise BadRequest()

        user_data = context.get_token_controller().use_register_token(token)
        try:
            User.get_by_email(context.get_db_connection(), user_data["email"])
        except NotFound:
            pass
        else:
            raise Gone() from None

        name = user_data.get("name", "Player")
        user = User.create(
            context.get_db_connection(), name=name, email=user_data["email"]
        )
        auth_token = user.create_auth_token(
            context.get_db_connection(),
            timedelta(days=30),
            request.headers["User-Agent"],
        )

        response = redirect(redirect_url)
        response.set_cookie(
            context.auth_token_name, auth_token, secure=is_production(), httponly=True
        )
        return response


class UserSignInApi(MethodView):
    def post(self):
        body = request.get_json()
        if body is None:
            raise BadRequest()
        email = body.get("email", None)
        if email is None:
            raise BadRequest()

        user = User.get_by_email(context.get_db_connection(), email)
        auth_token = user.create_auth_token(
            context.get_db_connection(),
            timedelta(days=30),
            request.headers["User-Agent"],
        )
        temp_auth_token = context.get_token_controller().new_signin_token(auth_token)
        context.send_auth_email(email, temp_auth_token)
        return ""

    def get(self):
        redirect_url = request.args.get("redirect", "/")
        token = request.args.get("token", None)
        if token is None:
            raise BadRequest()

        auth_token = context.get_token_controller().use_signin_token(token)

        response = redirect(redirect_url)
        response.set_cookie(
            context.auth_token_name, auth_token, secure=is_production(), httponly=True
        )
        return response


user_blueprint = Blueprint("user", __name__, url_prefix="user")
user_blueprint.add_url_rule("/", view_func=UserApi.as_view("user"))
user_blueprint.add_url_rule("signin/", view_func=UserSignInApi.as_view("user_sign_in"))
user_blueprint.add_url_rule(
    "register/", view_func=UserRegisterApi.as_view("user_register")
)
