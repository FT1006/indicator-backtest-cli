import logging
import os

def setup_logger(config):
    """
    Sets up logging based on a configuration dictionary.

    The configuration dictionary should have a "logging" section with:
      - level: Logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
      - format: Format string for log messages.
      - file: (Optional) File path to write logs to.

    Args:
        config (dict): The application configuration.

    Returns:
        logging.Logger: The configured root logger.
    """
    logging_config = config.get("logging", {})

    # Retrieve configuration values with defaults if not provided
    level_str = logging_config.get("level", "INFO").upper()
    log_format = logging_config.get("format", '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = logging_config.get("file")

    # Convert the string logging level to a logging module level constant
    level = getattr(logging, level_str, logging.INFO)
    
    # Obtain the root logger and set its level
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Remove pre-existing handlers to avoid duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create a formatter using the configuration format
    formatter = logging.Formatter(log_format)
    
    # Create a stream handler (console output)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # If a log file path is provided, add a file handler
    if log_file:
        # Ensure the directory for the log file exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
