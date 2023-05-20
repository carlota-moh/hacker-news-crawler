from logging import Logger
from datetime import datetime
from utils import Serializer
from crawler import Crawler
from data_parser import Retriever, Cleaner, Sorter

def main(url: str, logger: type[Logger]) -> None:
    # Instantiate crawler
    web_crawler = Crawler(logger=logger)

    # Get soup content
    web_crawler.get_soup(url=url)

    # Find required elements in soup
    entries = web_crawler.find_elements(element_name="tr", **{"class": "athing"})
    subtexts = web_crawler.find_elements(element_name="td", **{"class": "subtext"})

    # Retrieve dictionary with information from fields
    retriever = Retriever(logger=logger)
    all_entries_data = list(map(retriever.retrieve_entry_data, entries, subtexts))

    # Clean data in preparation for filtering
    cleaner = Cleaner(logger=logger)
    clean_entries = list(map(lambda e: cleaner.clean_fields(e, "rank", "points", "comments"), all_entries_data))

    # Filter and sort entries into separate lists
    sorter = Sorter(logger=logger)

    big_title_entries = list(filter(lambda dic: sorter.filter_dic(dic, field="title", limit=5), clean_entries))
    small_title_entries = [dic for dic in clean_entries if dic not in big_title_entries]

    sorted_big_title_entries = sorter.sort_by_field(big_title_entries, field="comments")
    sorted_small_title_entries = sorter.sort_by_field(small_title_entries, field="points")

    # save data to file
    serializer = Serializer(logger=logger)

    serializer.send_bulk_data(sorted_big_title_entries)
    serializer.send_bulk_data(sorted_small_title_entries)
     
if __name__=="__main__":
    import os
    from utils import CustomLogger, dir_maker
    
    # set paths
    data_dir = "./data/"
    log_dir = "./logs/"

    # make directories if needed
    dir_maker(data_dir)
    dir_maker(log_dir)
    
    # initialize logger
    logger_file = os.path.join(log_dir, "website-crawler.log")
    logger_name = "crawler"
    logger = CustomLogger(logger_file=logger_file, name=logger_name).logger

    url = "https://news.ycombinator.com/"

    # execute code
    main(url=url, logger=logger)

    

