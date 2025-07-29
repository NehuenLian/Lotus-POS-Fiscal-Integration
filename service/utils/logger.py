import logging
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# ===== Console Logger =====
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

console_logger = logging.getLogger('console_logger')
console_logger.setLevel(logging.DEBUG)
console_logger.addHandler(console_handler)
console_logger.propagate = False

# ===== File Logger =====
file_handler = TimedRotatingFileHandler(
    'service/invoice_service_logs/app.log', when='midnight', interval=1, backupCount=7, encoding='utf-8'
)
file_handler.setFormatter(formatter)

file_logger = logging.getLogger('file_logger')
file_logger.setLevel(logging.INFO)
file_logger.addHandler(file_handler)
file_logger.propagate = False
