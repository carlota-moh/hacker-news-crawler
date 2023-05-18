import unittest
from newscrawler.utils import Serializer, CustomLogger

class TestSerializer(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.logger = CustomLogger("test_logger", "test_logger.log").logger

    def test_serializer_init(self):
        serializer_instance = Serializer(self.logger)
        self.assertNotEqual(serializer_instance, None)
        self.assertEqual(serializer_instance.logger, self.logger)

    def test_serializer_serialize(self):
        serializer_instance = Serializer(self.logger)
        serializer_instance.serialize({"test": "serializer"}, "test.json")

        with open("test.json", "r") as f:
            self.assertEqual(f.read(), "{\"test\": \"serializer\"}")

    
if __name__ == '__main__':
    unittest.main()