import logging
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

business_file_handler = TimedRotatingFileHandler('src/POS_logs/business.log', when='midnight', interval=1, backupCount=7)
data_access_files_handler = TimedRotatingFileHandler('src/POS_logs/data_access.log', when='midnight', interval=1, backupCount=7)
controller_file_handler = TimedRotatingFileHandler('src/POS_logs/controller.log', when='midnight', interval=1, backupCount=7)

business_file_handler.setFormatter(formatter)
data_access_files_handler.setFormatter(formatter)
controller_file_handler.setFormatter(formatter)

console_logger = logging.getLogger('console')
console_logger.addHandler(console_handler)
console_logger.setLevel(logging.DEBUG)


business_logger = logging.getLogger('business')
business_logger.addHandler(business_file_handler)
business_logger.setLevel(logging.DEBUG)


data_access_logger = logging.getLogger('data_access')
data_access_logger.addHandler(data_access_files_handler)
data_access_logger.setLevel(logging.WARNING)


controller_logger = logging.getLogger('controller')
controller_logger.addHandler(controller_file_handler)
controller_logger.setLevel(logging.INFO)