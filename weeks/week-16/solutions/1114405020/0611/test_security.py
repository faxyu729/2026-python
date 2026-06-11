import unittest
import json
import os

from benchmark import make_data
from plot import load_results


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.test_json = "_sec_test.json"
        self.sample = {"key": "value"}

    def tearDown(self):
        if os.path.exists(self.test_json):
            os.remove(self.test_json)

    def test_make_data_rejects_negative(self):
        with self.assertRaises(ValueError):
            make_data(-5)

    def test_make_data_rejects_zero(self):
        with self.assertRaises(ValueError):
            make_data(0)

    def test_results_file_closed(self):
        with open(self.test_json, "w") as f:
            json.dump(self.sample, f)
        data = load_results(self.test_json)
        self.assertEqual(data, self.sample)
        os.remove(self.test_json)
        self.assertFalse(os.path.exists(self.test_json))

    def test_load_uses_json_not_pickle(self):
        with open(self.test_json, "w") as f:
            json.dump(self.sample, f)
        data = load_results(self.test_json)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
