from fastapi.testclient import TestClient
from main import app
import random
import string
import unittest
import time
import json

class TestFastAPI(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.client = TestClient(app)
        self._timestamp = time.time()
        self._test_json = self._create_test_json(title="Test Title")

    def _create_test_json(self, title: str = random.choice(string.ascii_letters)):
        return {
            "timestamp": self._timestamp,
            "title": title,
            "rank": 0,
            "points": 0,
            "comments": 0
        }

    def test_add_entry(self):
        response = self.client.post(
            "/add-entry/",
            json=self._test_json
        )
        self.assertEqual(response.status_code, 200)

    def test_add_existing_entry(self):
        response = self.client.post(
            "/add-entry/",
            json=self._test_json
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Entry already exists"})

    def test_add_entries_bulk(self):
        entry_1 = self._create_test_json()
        entry_2 = self._create_test_json()

        entries = [entry_1, entry_2]

        data = json.dumps(entries)
        response = self.client.post(
            "/add-entries-bulk/",
            headers={'Content-Type': 'application/json'},
            data=data
        )
        self.assertEqual(response.status_code, 200)
       

    def test_get_entries(self):
        response = self.client.get("/entries/")
        self.assertEqual(response.status_code, 200)

if __name__=="__main__":
    unittest.main()