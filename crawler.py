import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import logging
from typing import Optional, List
import re
import time

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

def get_text(entry, logger, element_name, **kwargs):
    """ Wrapper for retrieving text from entry element"""

    try:
        text = entry.find(element_name, **kwargs).get_text()
        return text
    
    except AttributeError as e:
        logger.warning(f"Encountered error while parsing: {e}")
        return "NA"

def retrieve_entry_data(entries: type[ResultSet], subtext: type[ResultSet], logger: logging.Logger) -> List[dict]:
    """ Retrieves relevant information from each of the elements """ 
    
    all_entries_data = []
    for entry, subtext in zip(entries, subtext):
        entry_data = {}
        
        entry_data["timestamp"] = time.time()
        title_entry = entry.find("span", {"class": "titleline"})
        entry_data["title"] = get_text(entry=title_entry, logger=logger, element_name="a")
        entry_data["rank"] = get_text(entry=entry, logger=logger, element_name="span", **{"class": "rank"})
        entry_data["points"] = get_text(entry=subtext, logger=logger, element_name="span", **{"class": "score"})
        entry_data["comments"] = get_text(entry=subtext, logger=logger, element_name="a", **{"string": re.compile(r'\bcomments\b')})
        all_entries_data.append(entry_data)
    
    return all_entries_data

if __name__ == "__main__":
    import os
    from utils import initialize_logger, write_json

    # set paths
    data_dir = "./data/"
    log_dir = "./logs/"
    
    # initialize logger
    logger_file = os.path.join(log_dir, "crawler.log")
    logger_name = "crawler"
    logger = initialize_logger(logger_file=logger_file, logger_name=logger_name)

    url = "https://news.ycombinator.com/"

    # retrieve HTML content
    soup = get_soup(url=url, logger=logger)

    # find elements in soup
    entries = find_elements(soup=soup, logger=logger, element_name="tr", **{"class": "athing"})
    subtext = find_elements(soup=soup, logger=logger, element_name="td", **{"class": "subtext"})

    all_entries_data = retrieve_entry_data(entries=entries, subtext=subtext, logger=logger)

    # write information to file
    json_path = os.path.join(data_dir, "./all_entries_data.json")
    write_json(dic=all_entries_data, file_path=json_path, logger=logger)


