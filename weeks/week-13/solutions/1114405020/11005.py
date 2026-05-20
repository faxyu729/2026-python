# -*- coding: utf-8 -*-
"""
UVA 11005 單元測試程式

測試方式：使用 importlib 載入同目錄下的 11005.py 進行測試。
"""

import unittest
import importlib.util
import os


def load_solution(name):
    """載入以數字開頭的 Python 解答模組"""
    path = os.path.join(os.path.dirname(__file__), f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"p{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# 載入 11005.py 中的函數
mod = load_solution("11005_hand")
cheapest_bases = mod.cheapest_bases
solve_all = mod.solve_all


class Test11005(unittest.TestCase):
    """UVA 11005 單元測試"""

    def test_zero_in_all_bases(self):
        """數字 0 在任何進位制都是 '0'，成本皆為 costs[0]"""
        costs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                 31, 32, 33, 34, 35, 36]
        result = cheapest_bases(0, costs)
        self.assertEqual(result, list(range(2, 37)))

    def test_fewest_digits_cheapest(self):
        """成本相同時，位數越少越省錢，100 在 11~36 進位只需 2 位數"""
        costs = [5] * 36
        result = cheapest_bases(100, costs)
        self.assertEqual(result, list(range(11, 37)))

    def test_decimal_is_cheapest(self):
        """讓 0-9 成本極低，使十進制成為最佳選擇"""
        costs = [1] * 10 + [100] * 26
        result = cheapest_bases(15, costs)
        self.assertIn(10, result)
        self.assertNotIn(16, result)

    def test_hex_is_cheapest(self):
        """讓 A-F 成本低，使十六進制成為最佳選擇"""
        costs = [100] * 10 + [1] * 6 + [100] * 20
        result = cheapest_bases(255, costs)
        self.assertIn(16, result)

    def test_sample(self):
        """範例測試：全部成本相同的情況"""
        sample = """1
1 2 3 4 5 6 7 8 9 10
10 10 10 10 10 10 10 10 10 10
10 10 10 10 10 10 10 10 10 10
10 10 10 10 10 10 10 10 10 10
3
0
10
100
"""
        out = solve_all(sample)
        self.assertIn("Case 1:", out)
        self.assertIn("Cheapest base(s) for number 0:", out)
        self.assertIn("Cheapest base(s) for number 10:", out)
        self.assertIn("Cheapest base(s) for number 100:", out)

    def test_large_number(self):
        """測試大數字（上限 2000000000），36 進位位數最少最省"""
        costs = [10] * 36
        result = cheapest_bases(2000000000, costs)
        self.assertEqual(result, [36])


if __name__ == "__main__":
    unittest.main()
