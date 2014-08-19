"""Interactive Brokers API Python package."""
import logging


# Default log level
LOG_LEVEL = logging.INFO


def configure_logging():
    """Configure the default logger for this package."""
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    handler = logging.NullHandler()
    line = '%(asctime)s %(levelname)s %(message)s'
    formatter = logging.Formatter(line)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# Setup logging
configure_logging()
