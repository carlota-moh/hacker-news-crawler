# Hacker news crawler

This is a small project dedicated towards scraping information from Hacker News [website](https://news.ycombinator.com/). The project consists of two modules that work together to perform crawling and parsing of the relevant content from the website:

+ crawler: The crawler is in charge of retrieving information from the first 30 entries in the web. In this case, we are only interested in retrieving the following fields: title, number in the order, number of comments and points.
+ parser: The parser will be in charge of performing transformations upon the retrieved information. First, it filters the entries according to whether or not the number of words in the title is above a specified cutoff (5, in this example). It thens orders each of the arrays according to a specified condition. In the implemented example, the array that contains entries having  more than 5 words in the title is ordered by number of comments in the entry, whereas the array that contains entries with less or equal to 5 words inside the title is ordered by the number of points.  
