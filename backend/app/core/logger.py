import logging
import sys
from typing import Optional


def setup_logger(name: str = "app", level: Optional[str] = None) -> logging.Logger:
    """Setup and return a configured logger"""
    logger = logging.getLogger(name)
    
    # Set level
    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler if not exists
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger


# Create default logger instance that can be imported directly
logger = setup_logger()