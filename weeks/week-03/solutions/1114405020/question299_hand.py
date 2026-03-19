#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 299 - 火車車廂排序 (手打版本)
"""

n = int(input())

for _ in range(n):
    l = int(input())

    if l == 0:
        print("Optimal train swapping takes 0 swaps.")
    else:
        arr = list(map(int, input().split()))
        swaps = 0

        for i in range(len(arr)):
            for j in range(len(arr) - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1

        print(f"Optimal train swapping takes {swaps} swaps.")
