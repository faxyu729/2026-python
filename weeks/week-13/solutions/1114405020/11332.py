# -*- coding: utf-8 -*-
"""
UVA 11332 單元測試程式

測試方式：使用 importlib 載入同目錄下的 11332.py 進行測試。
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


mod = load_solution("11332_hand")
solve_one_case = mod.solve_one_case


class Test11332(unittest.TestCase):
    """UVA 11332 單元測試"""

    def test_one_mirror_always_visible(self):
        """只有一個鏡子時一定可見"""
        result = solve_one_case([(1, 1, 3, 3)])
        self.assertEqual(result, [1])

    def test_two_mirrors_no_block(self):
        """兩個鏡子在不同方向，都可見"""
        result = solve_one_case([(1, 0, 1, 5), (5, 0, 5, 5)])
        self.assertEqual(result, [1, 1])

    def test_two_mirrors_blocked(self):
        """第二個鏡子被第一個擋住"""
        result = solve_one_case([(1, 1, 1, 3), (3, 1, 3, 3)])
        self.assertEqual(result[0], 1)

    def test_three_mirrors(self):
        """三個鏡子的基本測試"""
        result = solve_one_case([(1, 0, 1, 5), (5, 0, 5, 5), (10, 0, 10, 5)])
        self.assertEqual(result, [1, 1, 1])


if __name__ == "__main__":
    unittest.main()
