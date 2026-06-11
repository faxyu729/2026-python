import unittest
import os
import json

from plot import load_results, plot_results


class TestPlot(unittest.TestCase):
    def setUp(self):
        self.test_json = "_test_results.json"
        self.test_png = "_test_plot.png"
        self.sample_data = {
            "bubble_sort": {"500": 0.01, "1000": 0.07},
            "quick_sort": {"500": 0.001, "1000": 0.003},
        }

    def tearDown(self):
        for f in [self.test_json, self.test_png]:
            if os.path.exists(f):
                os.remove(f)

    def test_load_results_valid(self):
        with open(self.test_json, "w") as f:
            json.dump(self.sample_data, f)
        data = load_results(self.test_json)
        self.assertEqual(data, self.sample_data)

    def test_load_results_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_results("nonexistent.json")

    def test_load_results_invalid_json(self):
        with open(self.test_json, "w") as f:
            f.write("not json")
        with self.assertRaises(json.JSONDecodeError):
            load_results(self.test_json)

    def test_plot_creates_nonempty_png(self):
        data = self.sample_data
        plot_results(data, self.test_png)
        self.assertTrue(os.path.exists(self.test_png))
        self.assertGreater(os.path.getsize(self.test_png), 0)


if __name__ == "__main__":
    unittest.main()
