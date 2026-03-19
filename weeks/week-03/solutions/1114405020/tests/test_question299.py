#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 299 - 火車車廂排序 測試程式
"""

import unittest


def count_swaps(arr):
    """計算冒泡排序交換次數"""
    arr = arr[:]
    swaps = 0

    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return swaps


class TestQuestion299(unittest.TestCase):
    def test_sorted(self):
        """測試：已排序"""
        result = count_swaps([1, 2, 3])
        self.assertEqual(result, 0)

    def test_reverse_sorted(self):
        """測試：反向排序"""
        result = count_swaps([3, 2, 1])
        self.assertEqual(result, 3)

    def test_single_swap(self):
        """測試：單次交換"""
        result = count_swaps([2, 1])
        self.assertEqual(result, 1)

    def test_complex(self):
        """測試：複雜排列"""
        result = count_swaps([2, 3, 1])
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
