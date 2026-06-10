"""Stage 1 — @timeit 裝飾器測試

規格: timing.py 的 timeit 裝飾器必須
  1. 不改變被裝飾函式的回傳值
  2. 用 functools.wraps 保留 __name__ / __doc__
  3. 每次呼叫後更新 f.last_elapsed(float 秒)並 append 到 f.records
  4. 裝飾器內不准 print
"""

import time
import unittest

# from timing import timeit  # 完成 timing.py 後解除註解


class TestTimeit(unittest.TestCase):
    """@timeit 裝飾器功能驗證"""

    def test_returns_original_result(self):
        """裝飾後函式回傳值與原函式相同"""
        self.fail("尚未實作 — 自己打提示詞跟 AI 討論後補上")

    def test_preserves_function_metadata(self):
        """functools.wraps 保留 __name__ 與 __doc__"""
        self.fail("尚未實作")

    def test_last_elapsed_and_records_updated(self):
        """呼叫後 last_elapsed 為正 float, records append 該次耗時"""
        self.fail("尚未實作")

    def test_decorated_function_with_arguments(self):
        """有參數的函式仍正常執行並回傳正確值"""
        self.fail("尚未實作")

    # ── Edge cases ──

    def test_function_returning_none(self):
        """EDGE: 回傳 None 的函式仍正確記錄耗時"""
        self.fail("尚未實作")

    def test_initial_state_before_any_call(self):
        """EDGE: 尚未呼叫時 records 為空 list, last_elapsed 為 None"""
        self.fail("尚未實作")


if __name__ == "__main__":
    unittest.main()
