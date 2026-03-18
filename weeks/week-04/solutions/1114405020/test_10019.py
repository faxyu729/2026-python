import unittest
import importlib.util
import sys

# 載入標準版
import solution_10019

solve = solution_10019.solve

# 載入簡單版 (因為含有 '-' 無法直接 import)
try:
    spec = importlib.util.spec_from_file_location(
        "solution_10019_easy", "solution_10019-easy.py"
    )
    if spec and spec.loader:
        easy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(easy_module)
        solve_easy = easy_module.solve
except Exception:
    pass


class TestHashmat(unittest.TestCase):
    """
    這是一個針對 UVA 10055/10019 (Hashmat the Brave Warrior) 問題的單元測試。
    測試目標為驗證解題函式計算兩數差的絕對值是否正確。
    """

    def test_basic_difference(self):
        # 基本大小相減
        self.assertEqual(solve(10, 12), 2)
        self.assertEqual(solve_easy(10, 12), 2)

        self.assertEqual(solve(10, 14), 4)
        self.assertEqual(solve_easy(10, 14), 4)

        self.assertEqual(solve(100, 200), 100)
        self.assertEqual(solve_easy(100, 200), 100)

    def test_reverse_difference(self):
        # 參數反過來，預期仍為正數的差
        self.assertEqual(solve(12, 10), 2)
        self.assertEqual(solve_easy(12, 10), 2)

    def test_large_numbers(self):
        # 測試大數字 (題意 2^63)
        large_a = 2**62
        large_b = 2**63
        self.assertEqual(solve(large_a, large_b), 2**62)
        self.assertEqual(solve_easy(large_a, large_b), 2**62)

    def test_zero_difference(self):
        # 兩數相同
        self.assertEqual(solve(55, 55), 0)
        self.assertEqual(solve_easy(55, 55), 0)


if __name__ == "__main__":
    # 執行測試並保留紀錄
    with open("test_record_10019.log", "w", encoding="utf-8") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(argv=[""], testRunner=runner, exit=False)
