# -*- coding: utf-8 -*-
"""
UVA 11321 單元測試程式

測試方式：使用 importlib 載入同目錄下的 11321.py 進行測試。
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


mod = load_solution("11321_hand")
process_traps = mod.process_traps


class Test11321(unittest.TestCase):
    """UVA 11321 單元測試"""

    def test_small_path_exists(self):
        """小網格，放置陷阱後仍有路徑"""
        N, M = 3, 5
        traps = [(0, 0)]
        results = process_traps(N, M, traps)
        self.assertEqual(results, ["<(_ _)>"])

    def test_small_path_blocked(self):
        """阻擋唯一路徑"""
        N, M = 2, 3
        traps = [(0, 1), (1, 1)]
        results = process_traps(N, M, traps)
        self.assertEqual(results, ["<(_ _)>", ">_<"])

    def test_single_row(self):
        """單列網格（只有一條路）"""
        N, M = 1, 5
        traps = [(0, 2)]
        results = process_traps(N, M, traps)
        self.assertEqual(results, [">_<"])

    def test_multiple_rows_path(self):
        """多列網格，有替代路徑"""
        N, M = 3, 3
        traps = [(1, 0), (1, 2)]
        results = process_traps(N, M, traps)
        self.assertEqual(results, ["<(_ _)>", "<(_ _)>"])

    def test_no_effect(self):
        """無關的路徑不受影響"""
        N, M = 3, 4
        traps = [(0, 0)]
        results = process_traps(N, M, traps)
        self.assertEqual(results, ["<(_ _)>"])


if __name__ == "__main__":
    unittest.main()
