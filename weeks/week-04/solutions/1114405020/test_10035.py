import unittest
import importlib.util
import sys

# 載入標準版
import solution_10035

solve = solution_10035.solve

# 載入簡單版 (因為含有 '-' 無法直接 import)
try:
    spec = importlib.util.spec_from_file_location(
        "solution_10035_easy", "solution_10035-easy.py"
    )
    if spec and spec.loader:
        easy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(easy_module)
        count_carries = easy_module.count_carries
        get_output_message = easy_module.get_output_message

        def solve_easy(a, b):
            return get_output_message(count_carries(a, b))
except Exception:
    pass


class TestPrimaryArithmetic(unittest.TestCase):
    """
    針對 UVA 10035 (Primary Arithmetic) 問題的單元測試。
    測試目標為驗證進位次數計算以及輸出字串（單複數）是否符合題意。
    """

    def test_no_carry(self):
        # 測試完全沒有進位的情況
        self.assertEqual(solve(123, 456), "No carry operation.")
        self.assertEqual(solve_easy(123, 456), "No carry operation.")

        self.assertEqual(solve(0, 0), "No carry operation.")
        self.assertEqual(solve_easy(0, 0), "No carry operation.")

    def test_single_carry(self):
        # 測試只有 1 次進位的情況 (注意結尾沒有 s)
        self.assertEqual(solve(555, 544), "1 carry operation.")
        self.assertEqual(solve_easy(555, 544), "1 carry operation.")

        self.assertEqual(solve(9, 1), "1 carry operation.")
        self.assertEqual(solve_easy(9, 1), "1 carry operation.")

    def test_multiple_carries(self):
        # 測試多次進位的情況 (注意結尾有 s)
        self.assertEqual(solve(555, 555), "3 carry operations.")
        self.assertEqual(solve_easy(555, 555), "3 carry operations.")

    def test_cascading_carry(self):
        # 測試連鎖進位 (例如 999 + 1)
        self.assertEqual(solve(999, 1), "3 carry operations.")
        self.assertEqual(solve_easy(999, 1), "3 carry operations.")

    def test_different_length_numbers(self):
        # 測試不同長度的數字進位
        self.assertEqual(solve(999999, 1), "6 carry operations.")
        self.assertEqual(solve_easy(999999, 1), "6 carry operations.")

        self.assertEqual(solve(1, 999999), "6 carry operations.")
        self.assertEqual(solve_easy(1, 999999), "6 carry operations.")


if __name__ == "__main__":
    # 執行測試並保留紀錄
    with open("test_record_10035.log", "w", encoding="utf-8") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(argv=[""], testRunner=runner, exit=False)
