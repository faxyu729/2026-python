import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from task2_zipcode_heatmap import zip_to_county, load_county_counts, get_top_counties

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent.parent / "assets" / "stu-data"


class TestZipToCounty(unittest.TestCase):
    def test_zip_to_county_penghu(self):
        self.assertEqual(zip_to_county("880"), "澎湖縣")

    def test_zip_to_county_unknown(self):
        self.assertEqual(zip_to_county("999"), "其他")


class TestLoadCountyCounts(unittest.TestCase):
    def test_load_county_counts_type(self):
        result = load_county_counts(114, DATA_DIR)
        self.assertIsInstance(result, dict)

    def test_load_county_counts_penghu_positive(self):
        result = load_county_counts(114, DATA_DIR)
        penghu_count = result.get("澎湖縣", 0)
        self.assertGreater(penghu_count, 0)


class TestGetTopCounties(unittest.TestCase):
    def test_get_top_counties_length(self):
        year_data = {}
        for year in range(109, 115):
            year_data[year] = load_county_counts(year, DATA_DIR)
        top = get_top_counties(year_data, top_n=10)
        self.assertLessEqual(len(top), 10)
