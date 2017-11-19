import logging

logging.basicConfig(filename="sample.log", level=logging.INFO)
logging.debug(u'This is a debug message')
logging.info(u'This is an info message')
logging.warning(u'This is a warning')
logging.error(u'This is an error message')
logging.critical(u'FATAL!!!')
