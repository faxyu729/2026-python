"""Stage 2 — 排序正確性測試

規格: sorts.py 的 bubble_sort / quick_sort / merge_sort 必須
  1. 回傳新的排序後 list,不可修改傳入的 list
  2. 禁用內建 sorted() / list.sort()(那是 Stage 3 的對照組;
     測試裡拿 sorted() 當驗證標準則可以)

設計要求:三個函式共用同一組測試——用迴圈 + subTest,不要複製貼上三份。
"""

import unittest

from sorts import bubble_sort, quick_sort, merge_sort
from sorts_fast import bubble_sort_fast, quick_sort_fast

# 三個排序函式都放進這個 list,每個測試用 subTest 跑一輪;
# Stage 3 的加速版 append 進來就能吃到同一組測試。
SORT_FUNCTIONS = [bubble_sort, quick_sort, merge_sort,
                 bubble_sort_fast, quick_sort_fast]


class TestSortFunctions(unittest.TestCase):
    """三種排序共用同一組測試"""

    def test_basic_cases(self):
        """已排序、未排序、空 list、單一元素"""
        test_cases = [
            ([], []),
            ([1], [1]),
            ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
            ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
            ([3, 1, 4, 1, 5, 9], [1, 1, 3, 4, 5, 9]),
        ]

        for sort_func in SORT_FUNCTIONS:
            for data, expected in test_cases:
                with self.subTest(sort_func=sort_func.__name__, data=data):
                    result = sort_func(data)
                    self.assertEqual(result, expected)

    def test_random_data_matches_builtin(self):
        """亂數資料排序結果與 sorted() 一致"""
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(100)]

        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                result = sort_func(data)
                self.assertEqual(result, sorted(data))

    def test_input_not_mutated(self):
        """原始輸入 list 不可被排序函式修改"""
        original = [3, 1, 4, 1, 5]
        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                snapshot = original.copy()
                sort_func(original)
                self.assertEqual(original, snapshot)

    # ── Edge cases ──

    def test_all_identical_values(self):
        """EDGE: 所有元素相同"""
        data = [7] * 20
        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                result = sort_func(data)
                self.assertEqual(result, [7] * 20)

    def test_negative_and_mixed_numbers(self):
        """EDGE: 包含負數與零"""
        data = [0, -5, 3, -1, 2, -8, 7]
        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                result = sort_func(data)
                self.assertEqual(result, sorted(data))


if __name__ == "__main__":
    unittest.main()
