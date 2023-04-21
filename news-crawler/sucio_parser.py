import re
from typing import List

def remove_unicode(text: str) -> str:
    """ Function for removing unicode characters """
    return text.encode("ascii", "ignore").decode()

def get_numbers(text: str) -> int:
    match = re.match(r"^\d+", text)

    if match:
        return int(match.group())
    else:
        return 0
    
def filter_dic(dic: str, field: str, limit: int) -> bool:
    return True if len(dic[field]) > limit else False

def sort_by_field(entries_list: List[dict], field: str) -> List[dict]:
    return sorted(entries_list, key=lambda x: x[field], reverse=True)


def clean_fields(dic: dict) -> dict:
    """ 
    Function used for cleaning and preparing the fields'
    format   
    """
    # remove unicode characters
    clean_dict = dict((k, remove_unicode(v)) if isinstance(v, str) else (k, v) for k, v in dic.items())

    # apply additional formatting for rank and points
    clean_dict["rank"] = get_numbers(text=clean_dict["rank"])
    clean_dict["points"] = get_numbers(text=clean_dict["points"])
    clean_dict["comments"] = get_numbers(text=clean_dict["comments"])

    return clean_dict 

if __name__ == "__main__":
    import os
    from utils import initialize_logger, read_json

    # set paths
    data_dir = "./data/"
    log_dir = "./logs/"
    
    # initialize logger
    logger_file = os.path.join(log_dir, "data_parser.log")
    logger_name = "parser"
    logger = initialize_logger(logger_file=logger_file, logger_name=logger_name) 

    # load data
    json_path = os.path.join(data_dir, "./all_entries_data.json")
    all_entries_data = read_json(file_path=json_path, logger=logger)

    # clean fields
    all_entries_clean = list(map(clean_fields, all_entries_data))
    big_title_entries = list(filter(lambda dic: filter_dic(dic, field="title", limit=5), all_entries_clean))
    small_title_entries = [dic for dic in all_entries_clean if dic not in big_title_entries]
    sorted_big_title_entries = sort_by_field(big_title_entries, field="comments")
    sorted_small_title_entries = sort_by_field(big_title_entries, field="points")