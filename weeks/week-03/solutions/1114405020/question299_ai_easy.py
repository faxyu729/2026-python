#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 299 - 火車車廂排序 (AI簡化版本)

用於競賽練習的簡潔版本，包含詳細中文註解。

核心概念：
1. 冒泡排序並計數交換
2. 兩層迴圈掃過陣列
3. 每次交換就計數
"""

n = int(input())

for _ in range(n):
    l = int(input())

    if l == 0:
        print("Optimal train swapping takes 0 swaps.")
    else:
        arr = list(map(int, input().split()))
        swaps = 0

        # 冒泡排序
        for i in range(len(arr)):
            for j in range(len(arr) - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1

        print(f"Optimal train swapping takes {swaps} swaps.")
