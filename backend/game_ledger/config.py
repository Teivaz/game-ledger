from config import *

_defaults = {
    "base_url": "gameledger.app",
    "email": "system@gameledger.app",
}

cfg = ConfigurationSet(
    config_from_env(prefix="gameledger"),
    config_from_dict(_defaults),
)
