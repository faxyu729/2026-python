#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 299 - 火車車廂排序（Train Swapping）

問題描述：
    給定長度為L的火車車廂排列，需要計算最少相鄰交換次數
    才能將車廂排序為 1, 2, 3, ..., L。

    這等價於計算排列的逆序對(inversions)數量。

演算法說明：
    方法1：冒泡排序計數
    - 執行冒泡排序，每次交換就計數
    - 時間複雜度：O(L²)

    方法2：合併排序計數（更高效）
    - 使用分治思想
    - 時間複雜度：O(L log L)

    本實現使用冒泡排序計數法，易於理解和手寫。

時間複雜度：O(L²)，其中L為車廂數（最多50）
空間複雜度：O(L)
"""


def count_swaps_bubble_sort(arrangement):
    """
    使用冒泡排序計算交換次數。

    參數：
        arrangement (list)：當前車廂排列

    返回：
        int：所需的交換次數
    """
    arr = arrangement[:]  # 複製數組
    swaps = 0

    # 冒泡排序
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                # 交換
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return swaps


def solve_train_swapping():
    """
    主函數：讀取測資並計算交換次數。
    """
    try:
        n = int(input())

        for _ in range(n):
            l = int(input())

            if l == 0:
                print("Optimal train swapping takes 0 swaps.")
            else:
                arrangement = list(map(int, input().split()))
                swaps = count_swaps_bubble_sort(arrangement)
                print(f"Optimal train swapping takes {swaps} swaps.")

    except EOFError:
        pass


if __name__ == "__main__":
    solve_train_swapping()
