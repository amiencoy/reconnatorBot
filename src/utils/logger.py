import logging
import sys

def setup_logger(name="Reconnator"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler, ya udah sih handler aja
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Clean formatting biar ga keliatan plenger pas dibaca
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger