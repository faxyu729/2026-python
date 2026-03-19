#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 100 - 3n+1 問題 測試程式
"""

import unittest


def get_cycle_length(n, memo):
    """計算cycle-length"""
    if n in memo:
        return memo[n]

    if n == 1:
        return 1

    if n % 2 == 0:
        result = 1 + get_cycle_length(n // 2, memo)
    else:
        result = 1 + get_cycle_length(3 * n + 1, memo)

    memo[n] = result
    return result


class TestQuestion100(unittest.TestCase):
    """QUESTION-100 測試類"""

    def setUp(self):
        """每個測試前初始化快取"""
        self.memo = {1: 1}

    def test_cycle_length_1(self):
        """測試：n=1時Cycle-length為1"""
        result = get_cycle_length(1, self.memo)
        self.assertEqual(result, 1)

    def test_cycle_length_2(self):
        """測試：n=2"""
        result = get_cycle_length(2, self.memo)
        self.assertEqual(result, 2)

    def test_cycle_length_3(self):
        """測試：n=3"""
        result = get_cycle_length(3, self.memo)
        self.assertEqual(result, 8)

    def test_cycle_length_10(self):
        """測試：n=10"""
        result = get_cycle_length(10, self.memo)
        self.assertEqual(result, 7)

    def test_range_1_to_10(self):
        """測試：範圍[1,10]的最大Cycle-length"""
        max_len = 0
        for num in range(1, 11):
            max_len = max(max_len, get_cycle_length(num, self.memo))
        self.assertEqual(max_len, 20)

    def test_range_100_to_200(self):
        """測試：範圍[100,200]"""
        max_len = 0
        for num in range(100, 201):
            max_len = max(max_len, get_cycle_length(num, self.memo))
        self.assertEqual(max_len, 125)

    def test_caching_works(self):
        """測試：快取功能"""
        # 計算一次
        result1 = get_cycle_length(5, self.memo)
        # 第二次應該直接從快取返回
        result2 = get_cycle_length(5, self.memo)
        self.assertEqual(result1, result2)
        self.assertIn(5, self.memo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
