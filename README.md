# Hacker news crawler

This is a small project dedicated towards scraping information from Hacker News [website](https://news.ycombinator.com/). The project consists of several classes that work together to perform crawling and parsing of the relevant content from the website:

+ Crawler: The crawler is in charge of extracting the information from the HTML of the website. It can get the raw HTML content using `requests` and `BeautifulSoup` and the find the elements that are relevant to the specifications. 
+ Retriever: This class is in charge of retrieving the relevant fields from the parsed elements and organizing it into a dictionary. In this case, we are only interested in retrieving the following fields: title, number in the order, number of comments and points.
+ Cleaner: The cleaner is in charge of formatting and preparing the fields, taking care of removing unicode characters and converting numerical fields to `int` or `float`. 
+ Sorter: The sorter class takes care of filtering and sorting the lists of dictionaries.
+ Serializer: Finally, the serializer class is used for saving data to file.

To execute the code, run the following command from the root directory:

```bash
python3 news-crawler
```

The program will automatically create directories for storing data and program logs. Once executed, you can head to the `data/` directory and check the generated output files. If you do not wish to execute the code, I have already provided a couple of examples of the produced output within the `data/` directory. Feel free to check them out!

# Future improvements

Due to the time limitations, the implementations so far are limited. Future improvements upon this project would include:

1. Design automatic ingestion pipelines to periodically parse the content from the website. 

2. Developing unit-test for testing the different functionalities using libraries such as `unittest` or `pytest`

3. Implementing classes for modelling entries, which could be useful for future storage of content in databases using appropriate frameworks (e.g.: `django`)
