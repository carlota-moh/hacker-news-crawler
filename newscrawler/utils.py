import json
import logging
import requests
from os import makedirs
from os.path import exists
from typing import List

class CustomLogger:
    """ Class used for initializing logger object """
    def __init__(self, name: str, logger_file) -> None:
        self.name = name
        self.logger_file = logger_file
        self.logger = self.initialize_logger()
    
    def initialize_logger(self) -> None:
        """ Method used for handling logger configuration """

        # Initialize logger
        logger = logging.getLogger(name=self.name)
        logger.setLevel(logging.DEBUG)
        # Create a file handler to log the messages.
        file_handler = logging.FileHandler(self.logger_file)
        file_handler.setLevel(logging.DEBUG)
        # Create a console handler with a higher log level.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        # Modify the handlers log format to your convenience.
        handler_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            # "%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(lineno)s - %(message)s"
        )
        file_handler.setFormatter(handler_format)
        console_handler.setFormatter(handler_format)
        # Finally, add the handlers to the logger.
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

class Serializer:
    """ Class used for serializing data to file """
    def __init__(self, logger) -> None:
        self.logger = logger

    def serialize(self, dic: dict, file_path: str) -> None:
        """ Method used to write data to JSON in a specified filepath """
        try:
            with open(file_path, "w") as f:
                json.dump(dic, f)
                
            self.logger.info(f"Successfully written data to {file_path}")

        except FileNotFoundError:
            self.logger.error("Invalid path")

    def send_bulk_data(self, entries: List[dict]):
        """ Method used for sending data to backend """
        self.logger.info("Sending data to backend")
        url = "http://localhost:8000/add-entries-bulk/"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(entries)
        req = requests.post(url, headers=headers, data=data)
        
        if req.status_code == 200:
            self.logger.info("Successfully sent data to backend")
            
        else:
            self.logger.error("Failed to send data to backend" % req.status_code)

def dir_maker(dir_path: str) -> None:
    """ Auxiliary function for making directories """
    if not exists(dir_path):
        makedirs(dir_path)
    else:
        pass