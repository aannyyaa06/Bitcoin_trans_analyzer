import logging
from datetime import datetime
import pytz
from logging.handlers import TimedRotatingFileHandler

# Set up the loggig services
# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#For logging to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Add the formatter to the console handler
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)