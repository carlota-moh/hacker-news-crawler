import time
import re
from typing import List
from bs4 import ResultSet

class Retriever:
    """ Class for retrieving text from entries """
    def __init__(self, logger) -> None:
        self.logger = logger

    def get_text(self, entry: type[ResultSet], element_name: str, **kwargs) -> str:
        try:
            text = entry.find(element_name, **kwargs).get_text()
            return text
        
        except AttributeError as e:
            self.logger.warning(f"Encountered error while parsing: {e}")
            return "NA"
    
    def retrieve_entry_data(self, entry: type[ResultSet], subtext: type[ResultSet]) -> List[dict]:
        """ Retrieves relevant information from each entry """ 
        
        entry_data = {}
        entry_data["timestamp"] = time.time()
        title_entry = entry.find("span", {"class": "titleline"})
        entry_data["title"] = self.get_text(entry=title_entry, element_name="a")
        entry_data["rank"] = self.get_text(entry=entry, element_name="span", **{"class": "rank"})
        entry_data["points"] = self.get_text(entry=subtext, element_name="span", **{"class": "score"})
        entry_data["comments"] = self.get_text(entry=subtext, element_name="a", **{"string": re.compile(r'\bcomments\b')})
                    
        return entry_data
        

class Cleaner:
    """ Class used for cleaning up data prior to saving it in a class """
    def __init__(self, logger) -> None:
        self.logger = logger
        self.clean_dict = None

    def remove_unicode(self, text: str) -> str:
        """ Function for removing unicode characters """
        return text.encode("ascii", "ignore").decode()
    
    def get_numbers(self, text: str) -> int:
        match = re.match(r"^\d+", text)

        if match:
            return int(match.group())
        else:
            return 0

    def clean_fields(self, dic: dict, *numeric_fields) -> dict:
        """ 
        Function used for cleaning and preparing the fields'
        format   
        """
        # remove unicode characters
        clean_dict = dict((k, self.remove_unicode(v)) if isinstance(v, str) else (k, v) for k, v in dic.items())

        # apply additional formatting for numeric fields
        for field in numeric_fields:
            clean_dict[field] = self.get_numbers(text=clean_dict[field])

        self.clean_dict = clean_dict

class Sorter:
    """ Class used for filtering and sorting dictionaries """

    def __init__(self, logger) -> None:
        self.logger = logger

    def filter_dic(self, dic: str, field: str, limit: int) -> bool:
        """ Filter a dictionary by the value of specified field """
        if isinstance(dic[field], (int, float)):
            return True if len(dic[field]) > limit else False
        else:
            raise ValueError(
                f"field argument must be of type int or float. Found type {type(dic[field])}"
            )

    def sort_by_field(self, entries_list: List[dict], field: str, reverse: bool=True) -> List[dict]:
        """ Function used for sorting a list of entries according to the value of a field """
        return sorted(entries_list, key=lambda x: x[field], reverse=reverse)