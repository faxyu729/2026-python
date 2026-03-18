import unittest
import importlib.util
import sys

# 載入標準版
import solution_10038

solve = solution_10038.solve

# 載入簡單版
try:
    spec = importlib.util.spec_from_file_location(
        "solution_10038_easy", "solution_10038-easy.py"
    )
    if spec and spec.loader:
        easy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(easy_module)
        solve_easy = easy_module.is_jolly
except Exception:
    pass


class TestJollyJumpers(unittest.TestCase):
    """
    針對 UVA 10038 (Jolly Jumpers) 問題的單元測試。
    測試目標為驗證長度為 n 的序列，相鄰絕對差是否恰好涵蓋 1 到 n-1。
    """

    def test_jolly_sequence(self):
        # 4 個數字：1 4 2 3
        # 差的絕對值：3, 2, 1 (涵蓋 1~3)
        nums = [4, 1, 4, 2, 3]
        self.assertEqual(solve(nums), "Jolly")
        self.assertEqual(solve_easy(nums), "Jolly")

    def test_not_jolly_sequence(self):
        # 5 個數字：1 4 2 -1 6
        # 差的絕對值：3, 2, 3, 7 (沒有涵蓋 1~4，且有重複、有超出)
        nums = [5, 1, 4, 2, -1, 6]
        self.assertEqual(solve(nums), "Not jolly")
        self.assertEqual(solve_easy(nums), "Not jolly")

    def test_single_element(self):
        # 如果 n=1，永遠是 Jolly
        nums = [1, 42]
        self.assertEqual(solve(nums), "Jolly")
        self.assertEqual(solve_easy(nums), "Jolly")

    def test_duplicate_differences(self):
        # 差值有重複，沒有涵蓋全部
        # 4 個數字：1 2 3 4
        # 差的絕對值：1, 1, 1
        nums = [4, 1, 2, 3, 4]
        self.assertEqual(solve(nums), "Not jolly")
        self.assertEqual(solve_easy(nums), "Not jolly")

    def test_missing_differences(self):
        # 差值都大於範圍
        # 3 個數字：10 20 30
        # 差的絕對值：10, 10
        nums = [3, 10, 20, 30]
        self.assertEqual(solve(nums), "Not jolly")
        self.assertEqual(solve_easy(nums), "Not jolly")


if __name__ == "__main__":
    # 執行測試並保留紀錄
    with open("test_record_10038.log", "w", encoding="utf-8") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(argv=[""], testRunner=runner, exit=False)
