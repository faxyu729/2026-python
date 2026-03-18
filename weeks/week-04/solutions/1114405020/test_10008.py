import unittest
import importlib.util
import sys

# 載入標準版
import solution_10008

solve = solution_10008.solve

# 載入簡單版 (因為含有 '-' 無法直接 import)
spec = importlib.util.spec_from_file_location(
    "solution_10008_easy", "solution_10008-easy.py"
)
easy_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(easy_module)
solve_easy = easy_module.solve


class TestCryptanalysis(unittest.TestCase):
    """
    這是一個針對 UVA 10008 (密碼分析) 問題的單元測試。
    涵蓋大小寫轉換、過濾非字母字元、次數相同依字母排序等情境。
    """

    def test_basic_counting(self):
        # 簡單的大小寫計數測試
        lines = ["AaBbCc", "aBC"]
        # A: 3, B: 3, C: 3
        # 次數相同時，依照字母順序 A -> B -> C
        expected = [("A", 3), ("B", 3), ("C", 3)]
        self.assertEqual(solve(lines), expected)
        self.assertEqual(solve_easy(lines), expected)

    def test_filter_non_alpha(self):
        # 測試過濾掉標點符號與數字，僅計算字母
        lines = ["Hello, World 123!", "It's Python 3."]
        # 統計 (僅大寫):
        # H: 2, E: 1, L: 3, O: 3, W: 1, R: 1, D: 1, I: 1, T: 1, S: 1, P: 1, Y: 1, N: 1
        # 出現最多的應該是 L(3), O(3)，然後是 H(2)...
        expected = [
            ("L", 3),
            ("O", 3),
            ("H", 2),
            ("D", 1),
            ("E", 1),
            ("I", 1),
            ("N", 1),
            ("P", 1),
            ("R", 1),
            ("S", 1),
            ("T", 1),
            ("W", 1),
            ("Y", 1),
        ]
        self.assertEqual(solve(lines), expected)
        self.assertEqual(solve_easy(lines), expected)

    def test_empty_or_no_alpha(self):
        # 測試沒有任何字母的字串
        lines = ["123456", "   ", "!@#$%^&*()"]
        expected = []
        self.assertEqual(solve(lines), expected)
        self.assertEqual(solve_easy(lines), expected)

    def test_sorting_by_count(self):
        # 測試次數不同的排序，確保次數由大到小排在前面
        lines = ["Zz", "yYY", "x", "wwWw"]
        # W: 4, Y: 3, Z: 2, X: 1
        expected = [("W", 4), ("Y", 3), ("Z", 2), ("X", 1)]
        self.assertEqual(solve(lines), expected)
        self.assertEqual(solve_easy(lines), expected)


if __name__ == "__main__":
    # 執行測試並保留紀錄
    with open("test_record_10008.log", "w", encoding="utf-8") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(argv=[""], testRunner=runner, exit=False)
