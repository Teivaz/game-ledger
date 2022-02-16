import string, secrets
from typing import List, Any
from game_ledger.access_manager import AlManagedClass, AlManagedField, AccessLevel
from datetime import timedelta
from werkzeug.exceptions import *
import logging
_logger = logging.getLogger(__name__)
_alphabet = string.ascii_letters + string.digits
_token_size = 255

connection = Any # psycopg2 has problem with typing

class User(AlManagedClass):
    _fields = (
        AlManagedField("id", r=AccessLevel.users, w=AccessLevel.internal),
        AlManagedField("email", r=AccessLevel.private, w=AccessLevel.internal),
        AlManagedField("name", r=AccessLevel.users, w=AccessLevel.private),
        AlManagedField("profile_image", r=AccessLevel.users, w=AccessLevel.private),
        AlManagedField("parties", r=AccessLevel.private, w=AccessLevel.internal),
        AlManagedField("owned_games", r=AccessLevel.party, w=AccessLevel.private),
    )

    def __init__(self) -> None:
        self.id: int = 0
        self.email: str = ""
        self.name: str = ""
        self.profile_image: int = 0
        self.parties: List[int] = []
        self.owned_games: List[int] = []

    def __hash__(self):
        return self.id

    def get_access_level_for_user(self, user: "User"):
        if self.id == user.id:
            return AccessLevel.private
        if list(set(self.parties) & set(user.parties)):
            return AccessLevel.party
        else:
            return AccessLevel.users

    def create_auth_token(
        self, conn: connection, duration: timedelta, source: str
    ) -> str:
        _logger.debug("Creating auth token")
        token = "".join(secrets.choice(_alphabet) for i in range(_token_size))
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO user_sessions (token, duration, source, user_id)
                    values (%s, %s, %s, %s);
                    """,
                    (token, duration, source, self.id),
                )
        return token

    @staticmethod
    def auth_by_token(conn: connection, token: str) -> "User":
        _logger.debug("Auth by token")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT created, duration, source, user_id, (created + duration < now()) as expired
                FROM user_sessions
                WHERE token=%s;
                """,
                (token,),
            )
            if cur.rowcount == 0:
                raise NotFound()
            (created, duration, source, user_id, expired) = cur.fetchone()
            if expired:
                raise Gone()
        return User.get_by_id(conn, user_id)

    @staticmethod
    def get_by_email(conn: connection, email: str) -> "User":
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email = %s;", (email,))
            if cur.rowcount == 0:
                raise NotFound()
            (id,) = cur.fetchone()
        return User.get_by_id(conn, id)

    @staticmethod
    def get_by_id(conn: connection, user_id: int) -> "User":
        result = User()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    id,
                    email,
                    name,
                    profile_image,
                    (
                        SELECT coalesce(jsonb_agg(party_id), '[]'::jsonb)
                        FROM party_member
                        WHERE user_id = %s
                    ) as parties,
                    games
                FROM users
                WHERE id = %s;
                """,
                (user_id, user_id),
            )
            if cur.rowcount == 0:
                raise NotFound()
            (
                result.id,
                result.email,
                result.name,
                result.profile_image,
                result.parties,
                result.owned_games,
            ) = cur.fetchone()
        return result

    @staticmethod
    def create(conn: connection, name: str, email: str):
        _logger.debug("Creating user")
        result = User()
        result.name = name
        result.email = email
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (email, name) VALUES (%s, %s) RETURNING id;
                    """,
                    (
                        email,
                        name,
                    ),
                )
                (result.id,) = cur.fetchone()
        return result


    def save(self, conn: connection):
        _logger.info("Saving user")
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET email = %s, name = %s, profile_image = %s, games = %s
                    WHERE id = %s;
                    """,
                    (
                        self.email,
                        self.name,
                        self.profile_image,
                        self.id,
                        self.owned_games,
                    ),
                )

    def delete(self, conn: connection):
        _logger.info("Deleting user")
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (self.id,))
