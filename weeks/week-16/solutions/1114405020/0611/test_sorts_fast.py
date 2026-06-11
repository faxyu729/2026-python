import unittest
import copy

from sorts_fast import bubble_sort_fast, quick_sort_fast

SORT_FUNCTIONS = [bubble_sort_fast, quick_sort_fast]


class TestFastSorts(unittest.TestCase):
    def test_correctness(self):
        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort=sort_func.__name__):
                data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
                self.assertEqual(sort_func(data), sorted(data))

    def test_input_not_mutated(self):
        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort=sort_func.__name__):
                data = [3, 1, 4, 1, 5]
                original = copy.deepcopy(data)
                sort_func(data)
                self.assertEqual(data, original)

    def test_edge_cases(self):
        cases = [
            [],
            [42],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [7, 7, 7, 7],
        ]
        for sort_func in SORT_FUNCTIONS:
            for data in cases:
                with self.subTest(sort=sort_func.__name__, data=data):
                    self.assertEqual(sort_func(data), sorted(data))


if __name__ == "__main__":
    unittest.main()
