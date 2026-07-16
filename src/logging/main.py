from src.logging.logger import configure_logging
import logging

configure_logging()

logger = logging.getLogger(__name__)

logger.info("Application Started")