import json
import logging

class CustomLogger(logging.Logger):
    def __init__(self, name: str, logger_file: str) -> None:
        super().__init__(name)
        self.logger_file = logger_file
        self.logger = None
        self.initialize_logger()
    
    def initialize_logger(self) -> None:
        """ Used for easily initializing logger configuration """

        # Initialize logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        # Create a file handler to log the messages.
        log_file = self.logger_file
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
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)