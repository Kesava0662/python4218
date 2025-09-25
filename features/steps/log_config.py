import os
import logging
from datetime import datetime


def resolve_log_level(raw_config):
    log_levels = [lvl.strip() for lvl in raw_config.split(',')]
    severity_order = ['trace', 'debug', 'info', 'warn', 'error', 'fatal', 'off']
    for level in severity_order:
        if level in log_levels:
            return level
    return 'info'

log_level_map = {
    'trace': logging.DEBUG,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'fatal': logging.CRITICAL,
    'off': logging.NOTSET,
}

def setup_logger(log_level_raw):
    resolved_level = resolve_log_level(log_level_raw)
    python_level = log_level_map.get(resolved_level, logging.INFO)

    LOG_DIR = os.path.join(os.getcwd(), 'reports')
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Format: YYYYMMDD_HHMMSS
    log_file_name = f'report_{timestamp}.log'
    LOG_FILE_PATH = os.path.join(LOG_DIR, log_file_name)
    LOG_FORMAT = '%(asctime)s %(name)s %(levelname)s - %(message)s'
    logger = logging.getLogger('-')
    logger.setLevel(python_level)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

    return logger