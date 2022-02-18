import string, secrets
from typing import List, Any
from game_ledger.access_manager import AlManagedClass, AlManagedField, AccessLevel
from .user import User
from datetime import timedelta
from werkzeug.exceptions import *
import logging

_logger = logging.getLogger(__name__)
connection = Any  # psycopg2 has problem with typing


class Data(AlManagedClass):
    _fields = (
        AlManagedField("id", r=AccessLevel.users, w=AccessLevel.internal),
        AlManagedField("mime_type", r=AccessLevel.users, w=AccessLevel.internal),
        AlManagedField("content", r=AccessLevel.users, w=AccessLevel.internal),
        AlManagedField("owner", r=AccessLevel.users, w=AccessLevel.internal),
    )

    def __init__(self) -> None:
        self.id: int = 0
        self.mime_type: str = ""
        self.content: bytes = None
        self.owner: int = 0

    def __hash__(self):
        return self.id

    def get_access_level_for_user(self, user: "User"):
        return AccessLevel.users

    @staticmethod
    def get_by_id(conn: connection, data_id: int) -> "Data":
        result = Data()
        result.id = data_id
        with conn.cursor() as cur:
            cur.execute("SELECT content, type, owner FROM data WHERE id = %s;", (data_id,))
            if cur.rowcount == 0:
                raise NotFound()
            (
                result.content,
                result.mime_type,
                result.owner,
            ) = cur.fetchone()
        return result

    @staticmethod
    def create(conn: connection, user: User, content: bytes, mime_type: str):
        _logger.debug("Creating data")
        result = Data()
        result.content = content
        result.mime_type = mime_type
        result.owner = user.id
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO data (content, type, owner) VALUES (%s, %s, %s) RETURNING id;
                    """,
                    (
                        result.content,
                        result.mime_type,
                        result.owner,
                    ),
                )
                (result.id,) = cur.fetchone()
        return result

    @staticmethod
    def delete(conn: connection, user: User, id: int):
        _logger.info("Deleting data")
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM data WHERE id = %s and owner = %s", (id, user.id)
                )
