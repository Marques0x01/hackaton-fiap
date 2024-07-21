import logging

logger = logging.getLogger('morfina-service')
logger.setLevel(logging.INFO)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:%(funcName)s:%(lineno)d - %(asctime)s - %(name)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
