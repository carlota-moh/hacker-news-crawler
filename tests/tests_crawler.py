import unittest
from newscrawler.crawler import Crawler
from newscrawler.utils import CustomLogger

class TestCrawler(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.logger = CustomLogger("test_logger", "test_logger.log").logger

    def test_crawler_init(self):
        crawler_instance = Crawler(self.logger)
        self.assertNotEqual(crawler_instance, None)
        self.assertEqual(crawler_instance.logger, self.logger)
        self.assertEqual(crawler_instance.soup, None)

    def test_crawler_get_soup(self):
        crawler_instance = Crawler(self.logger)
        crawler_instance.get_soup("https://news.ycombinator.com/")
        self.assertNotEqual(crawler_instance.soup, None)

    def test_crawler_find_elements(self):
        crawler_instance = Crawler(self.logger)
        crawler_instance.get_soup("https://news.ycombinator.com/")
        elements = crawler_instance.find_elements("tr", **{"class": "athing"})
        self.assertNotEqual(elements, None)
        

if __name__ == '__main__':
    unittest.main()