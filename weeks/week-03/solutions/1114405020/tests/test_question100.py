import unittest
from uva100 import cycle_length, max_cycle_length


class TestUVA100(unittest.TestCase):
    """測試 UVA 100 (Collatz cycle length) 的相關函式。

    每一個測試均附有中文註解說明用途。
    此類別覆寫自 unittest.TestCase。
    """

    def test_cycle_length_example(self):
        # 測試 cycle_length 函式的基本邏輯
        # 22 的範例 sequence 長度應為 16
        self.assertEqual(cycle_length(22), 16)
        # 預期最小的正整數 1 有 cycle length 1
        self.assertEqual(cycle_length(1), 1)

    def test_max_cycle_length_samples(self):
        # 測試 max_cycle_length 在給定公開範例時的輸出是否正確
        # 此為 UVA/ZeroJudge 經典測資
        self.assertEqual(max_cycle_length(1, 10), 20)
        self.assertEqual(max_cycle_length(100, 200), 125)
        self.assertEqual(max_cycle_length(201, 210), 89)
        self.assertEqual(max_cycle_length(900, 1000), 174)

    def test_order_independence(self):
        # 驗證區間順序無關，函式應自行處理起迄值交換
        self.assertEqual(max_cycle_length(10, 1), 20)
        self.assertEqual(max_cycle_length(200, 100), 125)

    def test_small_ranges(self):
        # 測試小範圍的邊界情況：
        # - 單一數字，即 start == end
        # - 兩個相鄰數字
        self.assertEqual(max_cycle_length(5, 5), cycle_length(5))
        self.assertEqual(max_cycle_length(6, 7), max(cycle_length(6), cycle_length(7)))


if __name__ == "__main__":
    unittest.main()
