# -*- coding: utf-8 -*-
"""
UVA 11150 單元測試程式

測試方式：使用 importlib 載入同目錄下的 11150.py 進行測試。
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


mod = load_solution("11150_hand")
min_stones = mod.min_stones


class Test11150(unittest.TestCase):
    """UVA 11150 單元測試"""

    def test_no_stones(self):
        """完全沒有石子，答案應為 0"""
        self.assertEqual(min_stones(10, 1, 3, []), 0)

    def test_fixed_jump(self):
        """跳躍距離固定 S=T=2"""
        self.assertEqual(min_stones(10, 2, 2, [2, 4, 6]), 3)
        self.assertEqual(min_stones(10, 2, 2, [3, 5]), 0)

    def test_avoid_stone(self):
        """可以調整跳距避開石子的情況"""
        self.assertEqual(min_stones(10, 2, 3, [3]), 0)

    def test_must_hit_one_of_two(self):
        """石子在 2,3，跳距 1~2 時至少會踩到一顆"""
        self.assertEqual(min_stones(5, 1, 2, [2, 3]), 1)

    def test_avoid_sequence(self):
        """跳距 1~3 可以跳過孤立石子"""
        self.assertEqual(min_stones(10, 1, 3, [3, 6]), 0)

    def test_large_gap(self):
        """大間距壓縮測試：L 很大但石子很少"""
        self.assertEqual(min_stones(1000000000, 2, 5, [100, 200]), 0)


if __name__ == "__main__":
    unittest.main()
