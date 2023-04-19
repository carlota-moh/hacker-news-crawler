import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import logging
from typing import Optional, List

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
    logger.debug(f"Retrieving content from {url}")
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        logger.info(f"Successfully retrieved content from {url}")
        return soup
    else:
        logger.error("Something went wrong... Response code: {}".format(response.status_code))
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
    elements = soup.find_all(element_name, **kwargs)

    if len(elements) == 0:
        logger.warning(f"No {element_name} found")
        return None
    
    return elements

def retrieve_entry_data(entries: type[ResultSet], subtext: type[ResultSet]) -> List[dict]:
    """ Retrieves relevant information from each of the elements """ 
    
    all_entries_data = []
    for entry, subtext in zip(entries, subtext):
        entry_data = {}

        entry_data["title"] = entry.find("span", {"class": "titleline"}).find("a").get_text()
        entry_data["rank"] = entry.find("span", {"class": "rank"}).get_text()
        entry_data["points"] = subtext.find("span", {"class": "score"}).get_text()
        entry_data["comments"] = subtext.find(lambda tag: tag.name == "a" and "comment" in tag.text).get_text()
        all_entries_data.append(entry_data)
    
    return all_entries_data

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
    entries = find_elements(soup=soup, logger=logger, element_name="tr", **{"class": "athing"})
    subtext = find_elements(soup=soup, logger=logger, element_name="td", **{"class": "subtext"})

    all_entries_data = retrieve_entry_data(entries=entries, subtext=subtext)
