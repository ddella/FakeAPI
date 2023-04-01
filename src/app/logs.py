import logging
import platform

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:     %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.info(f'Python version: {platform.python_version()}')
logging.info(f'Hostname: {platform.node()}')
