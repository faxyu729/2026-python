#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 118 - 機器人模擬 (手打版本)
"""

try:
    x_max, y_max = map(int, input().split())

    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    dirs = "NESW"
    scents = set()

    while True:
        try:
            parts = input().split()
            x, y, d = int(parts[0]), int(parts[1]), parts[2]
            commands = input()

            di = dirs.index(d)

            for cmd in commands:
                if cmd == "L":
                    di = (di - 1) % 4
                elif cmd == "R":
                    di = (di + 1) % 4
                elif cmd == "F":
                    nx, ny = x + dx[di], y + dy[di]

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
