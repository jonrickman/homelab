import logging

from app.settings import settings

lvl = settings.logging_level
if lvl.lower() == "debug":
    # Set up logging configuration
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if lvl.lower() == "info":
    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if lvl.lower() == "warn":
    # Set up logging configuration
    logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if lvl.lower() == "error":
    # Set up logging configuration
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if lvl.lower() == "critical":
    # Set up logging configuration
    logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger instance
logger = logging.getLogger(__name__)

# This is noisy
logging.getLogger('pymongo').setLevel(logging.ERROR)
