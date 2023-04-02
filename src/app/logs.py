import logging
import platform

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:     %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger.info(f'Python version: {platform.python_version()}')
logger.info(f'Python implementation: {platform.python_implementation()}')
logger.info(f'Platform: {platform.platform()}')
logger.info(f'Hostname: {platform.node()}')
logger.info(f'System/OS name,: {platform.system()}')
logger.info(f'Release: {platform.release()}')
logger.info(f'Release Version: {platform.version()}')
logger.info(f'Uname: {platform.uname()}')
logger.info(f'Processor: {platform.machine()}')
try:
    OS_RELEASE = platform.freedesktop_os_release()
except OSError:
    pass
else:
    logger.info(f'OS Release: {OS_RELEASE}')
