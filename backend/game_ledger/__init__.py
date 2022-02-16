import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)
_logger.info("Created Logger")

from . import context
from .api import blueprint
