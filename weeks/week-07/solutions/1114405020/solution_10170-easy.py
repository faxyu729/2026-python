#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 10170 - 無限房間旅館 簡化版本

=== 核心思路 ===

旅館的住宿規則很簡單：
- 第 1 個團隊：S 人，住 S 天
- 第 2 個團隊：S+1 人，住 S+1 天
- 第 3 個團隊：S+2 人，住 S+2 天
- ...
- 第 i 個團隊：S+i-1 人，住 S+i-1 天

要找第 D 天住的團隊人數，需要找到哪個團隊在第 D 天。

=== 數學公式 ===

前 i 個團隊的總住宿天數：
sum = S + (S+1) + (S+2) + ... + (S+i-1)
    = i*S + (0+1+2+...+(i-1))
    = i*S + i(i-1)/2

只要找最小的 i 使得這個和 >= D，就能知道第 D 天是第 i 個團隊的人。

=== 演算法 ===

使用二分查找：
1. 設定搜尋範圍 [1, 某個上界]
2. 對於每個 mid，檢查前 mid 個團隊的天數是否 >= D
3. 如果 >= D，往左搜；否則往右搜
4. 最終得到的 i，返回 S + i - 1

=== 複雜度 ===

時間：O(log D) ≈ O(50)  (D 最大 10^15)
空間：O(1)
"""

import math
from typing import Optional


def sum_days(s: int, team_count: int) -> int:
    """
    計算前 team_count 個團隊的總住宿天數。

    公式：team_count * (2*s + team_count - 1) / 2

    參數：
        s: 第一個團隊的人數
        team_count: 前多少個團隊

    返回：
        總天數
    """
    return team_count * (2 * s + team_count - 1) // 2


def find_group_size(s: int, d: int) -> int:
    """
    找到第 D 天住的團隊人數。

    思路：
    1. 用二分查找找最小的 i 使得前 i 個團隊的日期 >= D
    2. 第 i 個團隊有 S + i - 1 人

    時間複雜度：O(log D)

    例子：
        find_group_size(4, 4)  → 4  (第 1-4 天是 4 人團隊)
        find_group_size(4, 5)  → 5  (第 5-9 天是 5 人團隊)
        find_group_size(4, 10) → 6  (第 10-15 天是 6 人團隊)
    """
    # 二分查找
    left = 1
    right = s + int(math.sqrt(2 * d)) + 100  # 估計上界

    while left < right:
        mid = (left + right) // 2

        # 檢查前 mid 個團隊的總天數
        if sum_days(s, mid) < d:
            # 還不夠，往右找
            left = mid + 1
        else:
            # 夠了，往左找更小的
            right = mid

    # left 就是最小的 i 使得前 i 個團隊的天數 >= D
    # 第 i 個團隊有 S + i - 1 人
    return s + left - 1


def main():
    """讀取輸入並輸出結果。"""
    import sys

    for line in sys.stdin:
        parts = line.strip().split()
        if len(parts) >= 2:
            s = int(parts[0])
            d = int(parts[1])
            print(find_group_size(s, d))


if __name__ == "__main__":
    main()
