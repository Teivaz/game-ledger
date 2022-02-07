from config import *

_defaults = {
    "base_url": "gameledger.app",
    "email": "system@gameledger.app",
    "postgres_host": "localhost",
    "postgres_port": "5432",
    "postgres_db": "game-ledger",
    "postgres_user": "admin",
    "postgres_password": "admin",
    "elasticemail_api_key": "00000000-0000-0000-0000-0000000000000",
}

cfg = ConfigurationSet(
    config_from_env(prefix="gameledger"),
    config_from_dict(_defaults),
)
