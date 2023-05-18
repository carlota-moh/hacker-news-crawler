import unittest
from newscrawler.utils import CustomLogger

class TestLogger(unittest.TestCase):

    def test_logger_init(self):
        logger_instance = CustomLogger("test_logger", "test_logger.log")
        self.assertNotEqual(logger_instance, None)
        self.assertEqual(logger_instance.name, "test_logger")
        self.assertEqual(logger_instance.logger_file, "test_logger.log")
        self.assertNotEqual(logger_instance.logger, logger_instance)

if __name__ == '__main__':
    unittest.main()