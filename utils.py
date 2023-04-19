import json
import logging

def initialize_logger(logger_file: str, logger_name: str) -> logging.Logger:
    """ Used for easily initializing logger """

    # Initialize logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # Create a file handler to log the messages.
    log_file = logger_file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    # Create a console handler with a higher log level.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    # Modify the handlers log format to your convenience.
    handler_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(handler_format)
    console_handler.setFormatter(handler_format)
    # Finally, add the handlers to the logger.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def write_json(dic: dict, file_path: str, logger: logging.Logger) -> None:
    """
    Function used to write data to JSON in a specified file_path

    Params:
    -dic: dictionary
        Python dictionary to be written to file

    -file_path: string
        final location of the file

    """
    try:
        with open(file_path, "w") as f:
            json.dump(dic, f)
        logger.info("Successfully written data to file")
    except FileNotFoundError:
        logger.error("Invalid path")

def read_json(file_path: str, logger: logging.Logger) -> dict:
    """
    Function used to read data from JSON in a specified file_path

    INPUTS:
    -file_path: string
        Location of the file
    -logger:
        Logger object

    RETURNS:
    -dic: dictionary
        Python dictionary containing information from JSON
    """
    try:
        with open(file_path, "r") as f:
            json_data = [json.loads(line) for line in f]
            return json_data
    except FileNotFoundError:
        logger.error("Could not read JSON. Invalid path to file")