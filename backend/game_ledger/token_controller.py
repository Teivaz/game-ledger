from typing import Dict
import string, secrets
from werkzeug.exceptions import *

_alphabet = string.ascii_letters + string.digits
_token_size = 64


def _create_temp_token():
    return "".join(secrets.choice(_alphabet) for i in range(_token_size))


class TokenController:
    def __init__(self) -> None:
        self.pending_signin_tokens: Dict[str, str] = {}  # temp_token: auth token
        self.pending_register_tokens: Dict[str, str] = {}  # temp_token: email
        self.pending_party_invites: Dict[str, int] = {}  # temp_token: party_id

    def new_party_invite(self, party_id: int) -> str:
        tok = _create_temp_token()
        self.pending_party_invites[tok] = party_id
        return tok

    def new_register_token(self, email: str) -> str:
        tok = _create_temp_token()
        self.pending_register_tokens[tok] = email
        return tok

    def new_signin_token(self, auth_token: str) -> str:
        tok = _create_temp_token()
        self.pending_register_tokens[tok] = auth_token
        return tok

    def use_party_invite(self, token: str) -> int:
        party_id = self.pending_party_invites.pop(token, None)
        if party_id is None:
            raise NotFound()
        return party_id

    def use_register_token(self, token: str) -> str:
        email = self.pending_register_tokens.pop(token, None)
        if email is None:
            raise NotFound()
        return email

    def use_signin_token(self, token: str) -> str:
        auth_token = self.pending_signin_tokens.pop(token, None)
        if auth_token is None:
            raise NotFound()
        return auth_token
