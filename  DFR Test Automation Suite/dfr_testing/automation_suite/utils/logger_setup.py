import logging
import sys
from dfr.testing.automation.config import global_config # Assuming dfr_testing.automation_suite is in PYTHONPATH or similar

# Ensure reports directory exists as logger might try to write files there.
# global_config.py already creates REPORTS_DIR, but defensive check here.
global_config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def setup_logger(name: str = 'DFR_Test_Logger', log_level: str = 'INFO', log_file: str = None):
    """
    Configures and returns a logger instance.

    Args:
        name (str): Name of the logger.
        log_level (str): Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR').
                        Defaults to 'INFO'.
        log_file (str, optional): Name of the log file (e.g., "test_run.log") to be created
                                  within the global_config.REPORTS_DIR.
                                  If None, logs only to console.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Prevent adding multiple handlers if logger is called multiple times with the same name
    if logger.hasHandlers():
        # Option 1: Clear existing handlers to reconfigure (e.g., if log_file or level changes)
        logger.handlers.clear()
        # Option 2: Return existing logger if already configured (simpler but less flexible for re-config)
        # return logger

    # Set level from string, default to INFO if invalid
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)8s] - %(module)s.%(funcName)s:%(lineno)d - %(message)s'
    )

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler
    if log_file:
        log_file_path = global_config.REPORTS_DIR / log_file
        try:
            fh = logging.FileHandler(log_file_path, mode='a') # Append mode
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except Exception as e:
            # Log to console if file handler fails
            sys.stderr.write(f"Warning: Could not initialize file logger at {log_file_path}: {e}\n")
            # Fallback to console logging only for this logger instance
    
    logger.propagate = False # Avoid duplicate logs if root logger is also configured (e.g., by pytest)
    return logger

# Example of a default logger instance for easy import if a generic logger is needed across modules
# test_suite_logger = setup_logger(log_file="dfr_test_suite.log")