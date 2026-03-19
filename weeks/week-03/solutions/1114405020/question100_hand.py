#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 100 - 3n+1 問題 (手打版本)

自己手寫的版本，基於簡化版的邏輯實現。
"""


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


memo = {1: 1}

try:
    while True:
        line = input().strip()
        if not line:
            continue

        i, j = map(int, line.split())
        start, end = min(i, j), max(i, j)

        max_len = 0
        for num in range(start, end + 1):
            max_len = max(max_len, get_cycle_length(num, memo))

        print(f"{i} {j} {max_len}")

except EOFError:
    pass
