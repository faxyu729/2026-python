"""
UVA 100 - 3n+1 (Collatz 序列) 的單元測試程式

本測試程式驗證計算 cycle-length 的正確性，以及在給定區間內找到最大 cycle-length 的功能。
"""

import unittest
import sys
from pathlib import Path

# 將上層目錄加入 Python 路徑，以便匯入同目錄的解題程式
sys.path.insert(0, str(Path(__file__).parent.parent))

from question100 import calculate_cycle_length, find_max_cycle_length


class TestCalculateCycleLength(unittest.TestCase):
    """
    測試 calculate_cycle_length 函式的單元測試類別。

    此類別測試單個數字的 cycle-length 計算是否正確。
    """

    def test_cycle_length_of_1(self):
        """
        測試 n=1 的情況。
        預期：cycle-length = 1（只有數字 1 本身）
        """
        self.assertEqual(calculate_cycle_length(1), 1)

    def test_cycle_length_of_2(self):
        """
        測試 n=2 的情況。
        數列：2 → 1
        預期：cycle-length = 2
        """
        self.assertEqual(calculate_cycle_length(2), 2)

    def test_cycle_length_of_3(self):
        """
        測試 n=3 的情況。
        數列：3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
        預期：cycle-length = 8
        """
        self.assertEqual(calculate_cycle_length(3), 8)

    def test_cycle_length_of_22(self):
        """
        測試 n=22 的情況（題目中的範例）。
        數列：22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 1
        預期：cycle-length = 16
        """
        self.assertEqual(calculate_cycle_length(22), 16)

    def test_cycle_length_of_10(self):
        """
        測試 n=10 的情況。
        數列：10 → 5 → 16 → 8 → 4 → 2 → 1
        預期：cycle-length = 7
        """
        self.assertEqual(calculate_cycle_length(10), 7)


class TestFindMaxCycleLength(unittest.TestCase):
    """
    測試 find_max_cycle_length 函式的單元測試類別。

    此類別測試在給定區間內找到最大 cycle-length 的功能。
    """

    def test_range_1_to_10(self):
        """
        測試區間 [1, 10] 的最大 cycle-length。
        預期結果：20
        """
        result = find_max_cycle_length(1, 10)
        self.assertEqual(result, 20)

    def test_range_100_to_200(self):
        """
        測試區間 [100, 200] 的最大 cycle-length。
        預期結果：125
        """
        result = find_max_cycle_length(100, 200)
        self.assertEqual(result, 125)

    def test_range_201_to_210(self):
        """
        測試區間 [201, 210] 的最大 cycle-length。
        預期結果：89
        """
        result = find_max_cycle_length(201, 210)
        self.assertEqual(result, 89)

    def test_range_900_to_1000(self):
        """
        測試區間 [900, 1000] 的最大 cycle-length。
        預期結果：174
        """
        result = find_max_cycle_length(900, 1000)
        self.assertEqual(result, 174)

    def test_range_reversed(self):
        """
        測試反序的區間（j < i 的情況）。
        輸入：find_max_cycle_length(10, 1)
        預期結果：應該與 find_max_cycle_length(1, 10) 相同，即 20
        """
        result = find_max_cycle_length(10, 1)
        self.assertEqual(result, 20)

    def test_single_element_range(self):
        """
        測試單一元素的區間（i == j）。
        輸入：find_max_cycle_length(5, 5)
        預期結果：n=5 的 cycle-length，即 6
        """
        result = find_max_cycle_length(5, 5)
        self.assertEqual(result, 6)


if __name__ == "__main__":
    # 執行所有單元測試並產生詳細的測試報告
    unittest.main(verbosity=2)
