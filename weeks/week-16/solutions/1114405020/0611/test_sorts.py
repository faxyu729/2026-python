import unittest
import copy

from sorts import bubble_sort, quick_sort, merge_sort

SORT_FUNCTIONS = [bubble_sort, quick_sort, merge_sort]


class TestSortFunctions(unittest.TestCase):
    def _run_all(self, data):
        original = copy.deepcopy(data)
        expected = sorted(data)
        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort=sort_func.__name__):
                result = sort_func(data)
                self.assertEqual(result, expected)

    def test_empty(self):
        self._run_all([])

    def test_single_element(self):
        self._run_all([42])

    def test_all_identical(self):
        self._run_all([5, 5, 5, 5])

    def test_already_sorted(self):
        self._run_all([1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        self._run_all([5, 4, 3, 2, 1])

    def test_with_duplicates(self):
        self._run_all([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])

    def test_random_data_matches_builtin(self):
        import random
        random.seed(42)
        data = [random.randint(0, 1000) for _ in range(100)]
        expected = sorted(data)
        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort=sort_func.__name__):
                result = sort_func(data)
                self.assertEqual(result, expected)

    def test_input_not_mutated(self):
        data = [3, 1, 4, 1, 5]
        original = copy.deepcopy(data)
        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort=sort_func.__name__):
                sort_func(data)
                self.assertEqual(data, original)


if __name__ == "__main__":
    unittest.main()
