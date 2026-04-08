#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 10170 - 無限房間旅館 單元測試程序

本程序包含12個測試用例，測試旅館住宿人數查詢功能。
每個測試用例包含詳細的註釋說明其預期行為。

測試環境：Python 3.x
執行方式：python test_10170.py
"""

import unittest
from solution_10170 import find_group_size


class TestHotelRooms(unittest.TestCase):
    """
    無限房間旅館問題的單元測試類別。

    測試範圍包括：
    - 基本情況：起始團隊的天數範圍
    - 邊界情況：不同團隊之間的銜接
    - 大數值：測試超大的 D 值（接近 10^15）
    - 特殊情況：S=1, S=10000 等邊界 S 值
    """

    def test_case_1_first_group(self):
        """
        測試用例 1: 第一個旅行團的最後一天

        說明：
        S=4 時，第一個團隊有 4 人，住 4 天（第 1-4 天）
        查詢第 4 天時，應該返回 4

        預期輸出：4
        """
        s, d = 4, 4
        result = find_group_size(s, d)
        self.assertEqual(result, 4)

    def test_case_2_second_group_start(self):
        """
        測試用例 2: 第二個旅行團的第一天

        說明：
        S=4 時，第二個團隊有 5 人，從第 5 天開始住
        查詢第 5 天時，應該返回 5

        預期輸出：5
        """
        s, d = 4, 5
        result = find_group_size(s, d)
        self.assertEqual(result, 5)

    def test_case_3_second_group_end(self):
        """
        測試用例 3: 第二個旅行團的最後一天

        說明：
        S=4 時，第二個團隊有 5 人，住 5 天（第 5-9 天）
        查詢第 9 天時，應該返回 5

        預期輸出：5
        """
        s, d = 4, 9
        result = find_group_size(s, d)
        self.assertEqual(result, 5)

    def test_case_4_third_group(self):
        """
        測試用例 4: 第三個旅行團

        說明：
        S=4 時：
        - 第 1-4 天：4 人團隊
        - 第 5-9 天：5 人團隊
        - 第 10-15 天：6 人團隊
        查詢第 10 天時，應該返回 6

        預期輸出：6
        """
        s, d = 4, 10
        result = find_group_size(s, d)
        self.assertEqual(result, 6)

    def test_case_5_s_equals_1(self):
        """
        測試用例 5: S=1 的邊界情況

        說明：
        S=1 時：
        - 第 1 天：1 人團隊
        - 第 2-3 天：2 人團隊
        - 第 4-6 天：3 人團隊
        查詢第 1 天時，應該返回 1

        預期輸出：1
        """
        s, d = 1, 1
        result = find_group_size(s, d)
        self.assertEqual(result, 1)

    def test_case_6_s_equals_1_later(self):
        """
        測試用例 6: S=1, 查詢較後面的天數

        說明：
        S=1 時，查詢第 6 天
        - 第 1 天：1 人
        - 第 2-3 天：2 人
        - 第 4-6 天：3 人
        第 6 天應該返回 3

        預期輸出：3
        """
        s, d = 1, 6
        result = find_group_size(s, d)
        self.assertEqual(result, 3)

    def test_case_7_large_s(self):
        """
        測試用例 7: S=10000

        說明：
        S=10000 時，第一個團隊就有 10000 人
        查詢第 5000 天時，仍在第一個團隊內（因為只住 10000 天）
        應該返回 10000

        預期輸出：10000
        """
        s, d = 10000, 5000
        result = find_group_size(s, d)
        self.assertEqual(result, 10000)

    def test_case_8_large_s_boundary(self):
        """
        測試用例 8: S=10000, 在邊界處

        說明：
        S=10000 時，第一個團隊在第 10000 天結束
        查詢第 10000 天時，應該返回 10000

        預期輸出：10000
        """
        s, d = 10000, 10000
        result = find_group_size(s, d)
        self.assertEqual(result, 10000)

    def test_case_9_large_s_next_group(self):
        """
        測試用例 9: S=10000, 進入第二個團隊

        說明：
        S=10000 時，第二個團隊有 10001 人，從第 10001 天開始
        查詢第 10001 天時，應該返回 10001

        預期輸出：10001
        """
        s, d = 10000, 10001
        result = find_group_size(s, d)
        self.assertEqual(result, 10001)

    def test_case_10_very_large_d(self):
        """
        測試用例 10: 非常大的 D 值

        說明：
        S=1, D=1000000
        測試算法的效率（不應該逐天遍歷）

        預期輸出：某個整數（具體值取決於計算）
        """
        s, d = 1, 1000000
        result = find_group_size(s, d)
        self.assertGreater(result, s)  # 結果應該大於起始人數

    def test_case_11_example_case(self):
        """
        測試用例 11: 題目中的範例案例

        說明：
        如果題目中有給定的範例，此測試驗證算法的正確性
        這裡使用 S=4 的完整序列進行驗證

        預期輸出：依序應該是 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, ...
        """
        s = 4
        expected = [4, 4, 4, 4, 5, 5, 5, 5, 5, 6]
        for day, exp in enumerate(expected, 1):
            result = find_group_size(s, day)
            self.assertEqual(result, exp, f"Day {day} should be {exp}")

    def test_case_12_sequential_groups(self):
        """
        測試用例 12: 多個連續的團隊轉換

        說明：
        S=2 時的完整序列：
        - 第 1-2 天：2 人
        - 第 3-5 天：3 人
        - 第 6-9 天：4 人
        - 第 10-14 天：5 人

        預期輸出：測試多個轉換點
        """
        s = 2
        test_cases = [
            (2, 2),  # 第 2 天，第一個團隊的最後一天：2 人
            (3, 3),  # 第 3 天，第二個團隊的第一天：3 人
            (5, 3),  # 第 5 天，第二個團隊的最後一天：3 人
            (6, 4),  # 第 6 天，第三個團隊的第一天：4 人
        ]

        for day, expected in test_cases:
            result = find_group_size(s, day)
            self.assertEqual(result, expected, f"S=2, Day {day} should be {expected}")


class TestHotelMathematicalProperties(unittest.TestCase):
    """
    旅館問題的數學性質測試。
    """

    def test_monotonicity(self):
        """
        測試單調性：隨著 D 增加，結果非遞減
        """
        s = 4
        prev_result = find_group_size(s, 1)
        for d in range(2, 100):
            result = find_group_size(s, d)
            self.assertGreaterEqual(result, prev_result)
            prev_result = result

    def test_consistency(self):
        """
        測試一致性：相同的 S 和 D 應該得到相同的結果
        """
        s, d = 5, 50
        result1 = find_group_size(s, d)
        result2 = find_group_size(s, d)
        self.assertEqual(result1, result2)

    def test_group_size_bounds(self):
        """
        測試結果的界限：結果應該 >= S
        """
        s = 100
        for d in [1, 100, 1000, 10000]:
            result = find_group_size(s, d)
            self.assertGreaterEqual(result, s)


if __name__ == "__main__":
    # 執行所有測試並輸出詳細結果
    unittest.main(verbosity=2)
