import unittest
from search import linear_search, binary_search

class TestSearch(unittest.TestCase):
    def test_linear_search_success(self):
        data = [10, 20, 30, 40, 50]
        self.assertEqual(linear_search(data, 10), 0) # 首
        self.assertEqual(linear_search(data, 30), 2) # 中
        self.assertEqual(linear_search(data, 50), 4) # 末

    def test_linear_search_fail(self):
        data = [10, 20, 30, 40, 50]
        self.assertEqual(linear_search(data, 60), -1) # 不存在

    def test_linear_search_empty(self):
        self.assertEqual(linear_search([], 10), -1) # 空

    def test_binary_search_success(self):
        data = [10, 20, 30, 40, 50]
        self.assertEqual(binary_search(data, 10), 0) # 首
        self.assertEqual(binary_search(data, 30), 2) # 中
        self.assertEqual(binary_search(data, 50), 4) # 末

    def test_binary_search_fail(self):
        data = [10, 20, 30, 40, 50]
        self.assertEqual(binary_search(data, 60), -1) # 不存在

    def test_binary_search_empty(self):
        self.assertEqual(binary_search([], 10), -1) # 空

    def test_binary_search_unsorted(self):
        data = [30, 10, 20]
        with self.assertRaises(ValueError):
            binary_search(data, 10) # 未排序拋錯

if __name__ == "__main__":
    unittest.main()
