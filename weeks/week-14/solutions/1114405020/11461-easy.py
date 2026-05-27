# -*- coding: utf-8 -*-
"""
11461 完全平方數（Square Numbers）—— 簡潔版

核心邏輯：用 sqrt() 找頭尾，再計算整數個數。
記憶要點：「ceil 頭、floor 尾，相減加一就 OK」。
"""

import math


def solve():
    """讀取標準輸入、計算完全平方數個數、輸出結果"""
    import sys
    for line in sys.stdin:
        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break
        # 計算 [a, b] 中完全平方數的個數
        cnt = math.floor(math.sqrt(b)) - math.ceil(math.sqrt(a)) + 1
        print(cnt)


if __name__ == "__main__":
    solve()
