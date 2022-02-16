from game_ledger.resources.user import User
from game_ledger.token_controller import TokenController
from game_ledger.config import cfg
from game_ledger.email import send_mail
from werkzeug.exceptions import *
from psycopg2 import connect
import flask
import typing as t


def init():
    context = {}

    context["db_connection"] = connect(
        host=cfg["postgres_host"],
        port=int(cfg["postgres_port"]),
        dbname=cfg["postgres_db"],
        user=cfg["postgres_user"],
        password=cfg["postgres_password"],
    )
    context["token_controller"] = TokenController()

    _init_db_tables(context["db_connection"])
    flask.current_app.context = context


def _init_db_tables(connection):
    # First check if tables exist and create if not
    # Perhaps we can use a db migration mechanism
    pass


def get_token_controller() -> TokenController:
    return flask.current_app.context["token_controller"]


def get_db_connection():
    return flask.current_app.context["db_connection"]


def send_auth_email(email: str, token: str):
    base_url = cfg["base_url"]
    send_mail(
        to_email=email,
        from_email=cfg["email"],
        from_name="Game Ledger System",
        subject="GameLedger Sign In Request",
        body_html=f'To sign in into the GameLedger please follow the link <a href="{base_url}/api/user/signin/?token={token}">Sign In</a>',
        body_text=f"To sign in into the GameLedger please enter the link in your browser\n{base_url}/api/user/signin/?token={token}\n",
    )


def send_register_email(email: str, token: str):
    base_url = cfg["base_url"]
    send_mail(
        to_email=email,
        from_email=cfg["email"],
        from_name="Game Ledger System",
        subject="GameLedger Sign Up Request",
        body_html=f'To proceed registering in GameLedger please follow the link <a href="{base_url}/api/user/register/?token={token}">Sign Up</a>',
        body_text=f"To proceed registering in GameLedger please enter the link in your browser\n{base_url}/api/user/register/?token={token}\n",
    )


auth_token_name = "gl_auth_token"


def get_current_user() -> t.Optional[User]:
    token = flask.request.cookies.get(auth_token_name)
    if token is None:
        return None
    try:
        return User.auth_by_token(get_db_connection(), token)
    except NotFound:
        return None
    except Gone:
        return None
