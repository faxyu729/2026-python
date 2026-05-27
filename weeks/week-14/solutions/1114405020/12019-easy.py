# -*- coding: utf-8 -*-
"""
12019 Doom's Day 演算法 —— 簡潔版

核心邏輯：從 Doomsday（星期三）偏移目標日期與 Doomsday 日期的差距。
記憶要點：「查表找日期，相減再偏移，模 7 取星期」。
"""

# 每月 Doomsday 日期（2012 年）
D = {1:10, 2:21, 3:7, 4:4, 5:9, 6:6,
     7:11, 8:8, 9:5, 10:10, 11:7, 12:12}

# 星期對照表（0=星期一 ~ 6=星期日）
W = ["Monday", "Tuesday", "Wednesday", "Thursday",
     "Friday", "Saturday", "Sunday"]


def solve():
    """讀取標準輸入、計算星期幾、輸出結果"""
    import sys
    data = sys.stdin.read().splitlines()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        m, d = map(int, data[i].split())
        # 2 = Wednesday（2012 年 Doomsday 的星期索引）
        out.append(W[(2 + d - D[m]) % 7])
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
