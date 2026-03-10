import unittest
from task3_log_summary import log_summary

class TestLogSummary(unittest.TestCase):
    def test_normal_case(self):
        input_data = """8
alice login
bob login
alice view
alice logout
bob view
bob view
chris login
bob logout"""
        expected = {
            "user_counts": [
                "bob 4",
                "alice 3",
                "chris 1"
            ],
            "top_action": "login 3"
        }
        self.assertEqual(log_summary(input_data), expected)

    def test_empty_logs(self):
        input_data = """0"""
        expected = {
            "user_counts": [],
            "top_action": "N/A 0"
        }
        self.assertEqual(log_summary(input_data), expected)

    def test_same_action(self):
        input_data = """3
alice login
bob login
chris login"""
        expected = {
            "user_counts": [
                "alice 1",
                "bob 1",
                "chris 1"
            ],
            "top_action": "login 3"
        }
        self.assertEqual(log_summary(input_data), expected)

if __name__ == '__main__':
    unittest.main()
