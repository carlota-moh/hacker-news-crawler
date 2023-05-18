import unittest
from newscrawler.data_parser import Retriever, Cleaner, Sorter
from newscrawler.utils import CustomLogger
from newscrawler.crawler import Crawler
import time
import re

class TestRetriever(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.logger = CustomLogger("test_logger", "test_logger.log").logger

    def test_retriever_init(self):
        retriever_instance = Retriever(logger=self.logger)
        self.assertNotEqual(retriever_instance, None)
        self.assertEqual(retriever_instance.logger, self.logger)

class TestCleaner(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.logger = CustomLogger("test_logger", "test_logger.log").logger
        self.retriever = Retriever(logger=self.logger)

    def test_cleaner_init(self):
        cleaner_instance = Cleaner(logger=self.logger)
        self.assertNotEqual(cleaner_instance, None)
        self.assertEqual(cleaner_instance.logger, self.logger)

    def test_cleaner_remove_unicode(self):
        cleaner_instance = Cleaner(logger=self.logger)
        test_string = "test \u2013string"
        self.assertEqual(cleaner_instance.remove_unicode(test_string), "test string")
    
    def test_cleaner_get_numbers(self):
        cleaner_instance = Cleaner(logger=self.logger)
        test_string = "123 test string"
        numbers = cleaner_instance.get_numbers(test_string)
        self.assertEqual(numbers, 123)
        self.assertIsInstance(numbers, int)

    def test_cleaner_clean_fields(self):
        cleaner_instance = Cleaner(logger=self.logger)
        test_dict = {"string": "test \u2013string", "numbers": "123 test string"}
        clean_dict = cleaner_instance.clean_fields(test_dict, "numbers")
        self.assertEqual(clean_dict, {"string": "test string", "numbers": 123})

class TestSorter(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.logger = CustomLogger("test_logger", "test_logger.log").logger
    
    def test_sorter_init(self):
        sorter_instance = Sorter(logger=self.logger)
        self.assertNotEqual(sorter_instance, None)
        self.assertEqual(sorter_instance.logger, self.logger)
    
    def test_sorter_filter_dict(self):
        sorter_instance = Sorter(logger=self.logger)
        test_dict = {"test": "this string has 5 words"}
        test_na = {"test": "NA"}
        self.assertEqual(sorter_instance.filter_dic(test_dict, "test", limit=2), True)
        self.assertEqual(sorter_instance.filter_dic(test_dict, "test", limit=5), False)
        self.assertEqual(sorter_instance.filter_dic(test_dict, "test", limit=10), False)
        self.assertEqual(sorter_instance.filter_dic(test_dict, "test", limit=10), False)
        self.assertEqual(sorter_instance.filter_dic(test_na, "test", limit=0), False)
        self.assertEqual(sorter_instance.filter_dic(test_na, "test", limit=10), False)

    def test_sorter_sort_by_field(self):
        sorter_instance = Sorter(logger=self.logger)
        entry_1 = {"test": 1}
        entry_2 = {"test": 2}
        entry_3 = {"test": 3}
        entry_list = [entry_2, entry_1, entry_3]
        self.assertEqual(sorter_instance.sort_by_field(entry_list, "test"), [entry_3, entry_2, entry_1])
        self.assertEqual(sorter_instance.sort_by_field(entry_list, "test", reverse=False), [entry_1, entry_2, entry_3])


if __name__=='__main__':
    unittest.main()

