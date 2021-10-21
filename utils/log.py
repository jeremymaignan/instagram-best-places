import logging
import os
import sys

import utils.config as conf

"""
Create logger with specific format
Log level set in conf or env
"""
logging.basicConfig(
    level=getattr(logging, conf.LOG_LEVEL.upper()),
    format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s'
)
logger = logging.getLogger()
