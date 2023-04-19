import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import logging
from typing import Optional

def get_soup(url: str, logger: logging.Logger) -> Optional[BeautifulSoup]:
    """
    Function used for loading HTML content into soup

    INPUTS:
    -url: string
        Desired url from whichi to retrieve HTML
    -logger:
        Logger object
    
    RETURNS:
    -soup:
        BeautifulSoup soup object with HTML content
    """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        logger.warning("Something went wrong... Response code: {}".format(response.status_code))
        return None

def find_elements(soup: type[BeautifulSoup], logger: logging.Logger, element_name: str, **kwargs) -> ResultSet:
    """
    Function used for finding elements by name within soup

    INPUTS:
    -soup:
        BeautifulSoup soup object with HTML content
    -logger:
        Logger object
    -element_name: string
        Name of the HTML tag by which to search for element
    -**kwargs:
        Other keyword arguments used for finding the element
    
    RETURNS:
    -elements: list
        List of elements in soup matching specified conditions
    """  
    try:
        elements = soup.find_all(element_name, **kwargs)
        if len(elements) == 0:
            logger.warning("No %s found") % element_name
        return elements
    except:
        logger.warning("No %s found") % element_name

if __name__=='__main__':
    from utils import initialize_logger
    # initialize logger

    logger_file = "./logs/crawler.log"
    logger_name = "crawler"
    logger = initialize_logger(logger_file=logger_file, logger_name=logger_name)

    url = "https://news.ycombinator.com/"

    # retrieve HTML content
    soup = get_soup(url=url, logger=logger)

    # find elements in soup
    tr_elements = find_elements(soup=soup, logger=logger, element_name="tr", **{"class": "athing"})