import logging

def get_logger(name: str = "bj") -> logging.Logger:
    logger = logging.Logger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(ch)
    return logger
