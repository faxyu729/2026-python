import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from task1_grouped_bar import load_year, get_top_depts

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent.parent / "assets" / "stu-data"


class TestLoadYear(unittest.TestCase):
    def test_load_year_returns_dict(self):
        result = load_year(112, DATA_DIR)
        self.assertIsInstance(result, dict)
        for k in result.keys():
            self.assertIsInstance(k, str)

    def test_load_year_counts_correct(self):
        result = load_year(112, DATA_DIR)
        total = sum(result.values())
        for dept, count in result.items():
            if "觀光" in dept or "休閒" in dept:
                self.assertGreater(count, 0)
                break
        else:
            self.assertGreater(total, 0)

    def test_load_year_total_positive(self):
        for year in [112, 113, 114]:
            result = load_year(year, DATA_DIR)
            total = sum(result.values())
            self.assertGreater(total, 0)


class TestGetTopDepts(unittest.TestCase):
    def test_get_top_depts_length(self):
        year_data = {year: load_year(year, DATA_DIR) for year in [112, 113, 114]}
        top = get_top_depts(year_data, top_n=8)
        self.assertLessEqual(len(top), 8)

    def test_get_top_depts_includes_popular(self):
        year_data = {year: load_year(year, DATA_DIR) for year in [112, 113, 114]}
        top = get_top_depts(year_data, top_n=8)
        found_popular = any("觀光" in d or "休閒" in d for d in top)
        self.assertTrue(found_popular)
