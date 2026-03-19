#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 118 - 機器人模擬 (AI簡化版本)

用於競賽練習的簡潔版本，包含詳細中文註解。

核心概念：
1. 方向編號：N=0, E=1, S=2, W=3
2. 左轉時減1再模4，右轉時加1再模4
3. 使用座標對(x,y)的集合記錄scent位置
4. 前進時檢查邊界和scent標記
"""

try:
    x_max, y_max = map(int, input().split())

    # 方向：北(0), 東(1), 南(2), 西(3)
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    dirs = "NESW"
    scents = set()

    while True:
        try:
            parts = input().split()
            x, y, d = int(parts[0]), int(parts[1]), parts[2]
            commands = input()

            # 取得方向編號
            di = dirs.index(d)

            for cmd in commands:
                if cmd == "L":
                    di = (di - 1) % 4
                elif cmd == "R":
                    di = (di + 1) % 4
                elif cmd == "F":
                    nx, ny = x + dx[di], y + dy[di]

                    # 檢查邊界
                    if nx < 0 or nx > x_max or ny < 0 or ny > y_max:
                        if (x, y) not in scents:
                            scents.add((x, y))
                            print(f"{x} {y} {dirs[di]} LOST")
                            break
                    else:
                        x, y = nx, ny
            else:
                print(f"{x} {y} {dirs[di]}")

        except EOFError:
            break

except EOFError:
    pass
