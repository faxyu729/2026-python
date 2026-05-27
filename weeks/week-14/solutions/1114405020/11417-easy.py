# -*- coding: utf-8 -*-
"""
11417 GCD 總和 —— 簡潔版

核心邏輯：雙層迴圈窮舉所有數對 (i, j)，用 math.gcd() 加總。
記憶要點：「雙層迴圈 i < j，gcd 累加就搞定」。
"""

import math


def solve():
    """讀取標準輸入、計算 GCD 總和、輸出結果"""
    import sys
    for line in sys.stdin:
        n = int(line.strip())
        if n == 0:
            break
        total = 0
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                total += math.gcd(i, j)
        print(total)


if __name__ == "__main__":
    solve()
