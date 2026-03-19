#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 100 - 3n+1 問題 (AI簡化版本)

用於競賽練習的簡潔版本，包含詳細中文註解。

核心概念：
1. 計算Cycle-length（從n到1的步數）
2. 使用記憶化快取優化重複計算
3. 對每個查詢範圍找出最大Cycle-length
"""


def cycle_length(n, cache):
    """
    計算n的Cycle-length（到1為止的步數）。

    參數：
        n (int)：起始數字
        cache (dict)：記憶化快取，存儲已計算的結果

    返回：
        int：Cycle-length
    """
    # 基礎情況：如果已在快取中，直接返回
    if n in cache:
        return cache[n]

    # 基礎情況：1的Cycle-length是1
    if n == 1:
        return 1

    # 遞迴計算
    if n % 2 == 0:
        # 偶數：n/2
        result = 1 + cycle_length(n // 2, cache)
    else:
        # 奇數：3n+1
        result = 1 + cycle_length(3 * n + 1, cache)

    # 存入快取
    cache[n] = result
    return result


def main():
    """主函數：讀取輸入並計算結果。"""
    cache = {1: 1}  # 初始快取：1的Cycle-length是1

    try:
        while True:
            line = input().strip()
            if not line:
                continue

            # 解析輸入：兩個整數 i 和 j
            i, j = map(int, line.split())

            # 確保 i <= j（題目可能輸入任意順序）
            start, end = min(i, j), max(i, j)

            # 計算範圍內的最大Cycle-length
            max_length = 0
            for num in range(start, end + 1):
                max_length = max(max_length, cycle_length(num, cache))

            # 輸出結果：格式為 i j max_length
            print(f"{i} {j} {max_length}")

    except EOFError:
        pass


if __name__ == "__main__":
    main()
