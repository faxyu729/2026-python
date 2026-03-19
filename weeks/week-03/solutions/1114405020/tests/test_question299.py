#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 299 - 火車車廂排序 測試檔

測試交換次數計算：
1. 空列表（L=0）
2. 已排序列表
3. 反向排序列表
4. 隨機排列
5. 單一元素
"""

import unittest


def count_swaps_bubble_sort(arrangement):
    """
    使用冒泡排序計算交換次數。

    參數：
        arrangement (list)：當前車廂排列

    返回：
        int：所需的交換次數
    """
    arr = arrangement[:]
    swaps = 0

    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return swaps


class TestTrainSwapping(unittest.TestCase):
    """火車車廂排序測試類"""

    def test_empty_list(self):
        """測試：空列表"""
        result = count_swaps_bubble_sort([])
        self.assertEqual(result, 0)

    def test_single_element(self):
        """測試：單一元素"""
        result = count_swaps_bubble_sort([1])
        self.assertEqual(result, 0)

    def test_sorted_list(self):
        """測試：已排序列表"""
        result = count_swaps_bubble_sort([1, 2, 3, 4, 5])
        self.assertEqual(result, 0)

    def test_reverse_sorted_list(self):
        """測試：反向排序列表"""
        # [5, 4, 3, 2, 1] 需要 4+3+2+1 = 10 次交換
        result = count_swaps_bubble_sort([5, 4, 3, 2, 1])
        self.assertEqual(result, 10)

    def test_simple_swap(self):
        """測試：單次交換"""
        # [2, 1, 3] → [1, 2, 3] 需要 1 次交換
        result = count_swaps_bubble_sort([2, 1, 3])
        self.assertEqual(result, 1)

    def test_example_2_4_1_3(self):
        """測試：例子 [2, 4, 1, 3]"""
        # [2, 4, 1, 3]
        # [2, 1, 4, 3] - 交換1次
        # [2, 1, 3, 4] - 交換2次
        # [1, 2, 3, 4] - 交換3次
        result = count_swaps_bubble_sort([2, 4, 1, 3])
        self.assertEqual(result, 3)

    def test_example_3_2_1(self):
        """測試：例子 [3, 2, 1]"""
        # [3, 2, 1] → 需要 3 次交換
        result = count_swaps_bubble_sort([3, 2, 1])
        self.assertEqual(result, 3)

    def test_example_1_3_2(self):
        """測試：例子 [1, 3, 2]"""
        # [1, 3, 2] → [1, 2, 3] 需要 1 次交換
        result = count_swaps_bubble_sort([1, 3, 2])
        self.assertEqual(result, 1)

    def test_two_elements_sorted(self):
        """測試：兩個已排序元素"""
        result = count_swaps_bubble_sort([1, 2])
        self.assertEqual(result, 0)

    def test_two_elements_unsorted(self):
        """測試：兩個未排序元素"""
        result = count_swaps_bubble_sort([2, 1])
        self.assertEqual(result, 1)

    def test_large_small_pattern(self):
        """測試：大-小-大-小 模式"""
        # [2, 1, 4, 3, 6, 5]
        result = count_swaps_bubble_sort([2, 1, 4, 3, 6, 5])
        # 每對需要1次交換：共3次交換
        self.assertEqual(result, 3)

    def test_complex_arrangement(self):
        """測試：複雜排列"""
        result = count_swaps_bubble_sort([4, 3, 2, 1])
        # 需要 3+2+1 = 6 次交換
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
