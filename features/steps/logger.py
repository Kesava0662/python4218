import json
import logging
import os
import allure


logger = None


def format_message(*args):
    return ' | '.join(
        json.dumps(arg, indent=2) if isinstance(arg, (dict, list, tuple, set)) else str(arg)
        for arg in args if arg is not None
    )


def get_logger(log_file_path='reports/report.log'):
    global logger
    if logger:
        return logger

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    logger = logging.getLogger("-")

    if not logger.handlers:
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def info(context, *args):
    log = get_logger()
    message = format_message(*args)
    log.info(message)
    _attach_allure(context, message, "Info")
    _append_to_context(context, message)

def error(context, *args):
    log = get_logger()
    message = format_message(*args)
    log.error(message)
    _attach_allure(context, message, "Error")
    _append_to_context(context, message)

def debug(context, *args):
    log = get_logger()
    message = format_message(*args)
    log.debug(message)
    _attach_allure(context, message, "Debug")

def warn(context, *args):
    log = get_logger()
    message = format_message(*args)
    log.warning(message)
    _attach_allure(context, message, "Warning")

def _attach_allure(context, message, name):
    try:
        allure.attach(message, name=name, attachment_type=allure.attachment_type.TEXT)
    except Exception as e:
        print(f"[Allure Attach Fail - {name}] {e}")

def _append_to_context(context, message):
    try:
        # CHANGED: context.eachStepMessage -> context.each_step_message
        context.each_step_message.append(message)
    except Exception as e:
        print(f"[Context Append Fail] {e}")

def log_info(*args):
    log = get_logger()
    message = format_message(*args)
    log.info(message)

def log_error(*args):
    log = get_logger()
    message = format_message(*args)
    log.error(message)

def log_debug(*args):
    log = get_logger()
    message = format_message(*args)
    log.debug(message)