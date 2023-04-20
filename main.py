if __name__=="__main__":
    import os
    from utils import initialize_logger, write_json
    from crawler import Crawler
    from data_parser import Retriever, Cleaner, Sorter
    from data_structure import Entry, EntryEncoder, Serializer

    # set paths
    data_dir = "./data/"
    log_dir = "./logs/"
    
    # initialize logger
    logger_file = os.path.join(log_dir, "crawler.log")
    logger_name = "crawler"
    logger = initialize_logger(logger_file=logger_file, logger_name=logger_name)

    url = "https://news.ycombinator.com/"

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
    sorted_small_title_entries = sorter.sort_by_field(big_title_entries, field="points")

    print(sorted_big_title_entries, '\n')
    print(sorted_small_title_entries, '\n')


