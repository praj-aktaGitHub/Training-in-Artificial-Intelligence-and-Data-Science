import logging

logging.basicConfig(
    filename = 'applog',
    level = logging.INFO,
    format = '%(asctime)s%(levelname)s%(message)s'
)
logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')