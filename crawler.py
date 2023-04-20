import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import logging
from typing import Optional, List
import re
import time

class Crawler:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.soup = None

    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """
        Function used for loading HTML content into soup

        INPUTS:
        -url: string
            Desired url from whichi to retrieve HTML
        
        RETURNS:
        -soup:
            BeautifulSoup soup object with HTML content
        """
        self.logger.debug(f"Retrieving content from {url}")
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            self.logger.info(f"Successfully retrieved content from {url}")
            self.soup = soup
        else:
            self.logger.error("Something went wrong... Response code: {}".format(response.status_code))
            self.soup = None

    def find_elements(self, element_name: str, **kwargs) -> ResultSet:
        """
        Function used for finding elements by name within soup

        INPUTS:
        -element_name: string
            Name of the HTML tag by which to search for element
        -**kwargs:
            Other keyword arguments used for finding the element
        
        RETURNS:
        -elements: list
            List of elements in soup matching specified conditions
        """  
        elements = self.soup.find_all(element_name, **kwargs)

        if len(elements) == 0:
            self.logger.warning(f"No {element_name} found")
            return None
        
        return elements

