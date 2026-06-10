"""Stage 3 — 加速版排序正確性測試

規格: sorts_fast.py 的加速版排序必須
  1. 與原始排序結果完全一致
  2. 回傳新的 list,不可修改輸入
  3. 通過與 Stage 2 相同的正確性驗證

加速方案(演算法優化):
  - bubble_sort_fast: 提前停止(無交換就結束)
  - quick_sort_fast: median-of-three 選 pivot + 小區間切 insertion sort
"""

import unittest

from sorts_fast import bubble_sort_fast, quick_sort_fast

FAST_FUNCTIONS = [bubble_sort_fast, quick_sort_fast]


class TestFastSortFunctions(unittest.TestCase):
    """加速版排序共用同一組測試"""

    def test_basic_cases(self):
        """已排序、未排序、空 list、單一元素"""
        test_cases = [
            ([], []),
            ([1], [1]),
            ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
            ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
            ([3, 1, 4, 1, 5, 9], [1, 1, 3, 4, 5, 9]),
        ]

        for sort_func in FAST_FUNCTIONS:
            for data, expected in test_cases:
                with self.subTest(sort_func=sort_func.__name__, data=data):
                    result = sort_func(data)
                    self.assertEqual(result, expected)

    def test_random_data_matches_builtin(self):
        """亂數資料排序結果與 sorted() 一致"""
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(100)]

        for sort_func in FAST_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                result = sort_func(data)
                self.assertEqual(result, sorted(data))

    def test_input_not_mutated(self):
        """原始輸入 list 不可被排序函式修改"""
        original = [3, 1, 4, 1, 5]
        for sort_func in FAST_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                snapshot = original.copy()
                sort_func(original)
                self.assertEqual(original, snapshot)

    # ── Edge cases ──

    def test_all_identical_values(self):
        """EDGE: 所有元素相同"""
        data = [7] * 20
        for sort_func in FAST_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                result = sort_func(data)
                self.assertEqual(result, [7] * 20)

    def test_large_random_data(self):
        """EDGE: 大量亂數(1000 筆)"""
        import random
        random.seed(99)
        data = [random.randint(-5000, 5000) for _ in range(1000)]

        for sort_func in FAST_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                result = sort_func(data)
                self.assertEqual(result, sorted(data))


if __name__ == "__main__":
    unittest.main()
