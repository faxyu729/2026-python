#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 118 - 機器人模擬

問題描述：
    在一個矩形網格中模擬多個機器人的移動。機器人可以接收指令：
    - L：左轉90度
    - R：右轉90度
    - F：前進一格

    當機器人走出邊界時會掉落消失，但會在最後位置留下標記。
    其他機器人若在有標記的位置執行會導致掉落的動作，該動作會被忽略。

演算法說明：
    1. 使用字典存儲方向向量和方向索引
    2. 使用集合存儲掉落位置（scent位置）
    3. 對每個機器人，依序執行指令
    4. 檢查邊界條件和scent標記

時間複雜度：O(N * L)，其中N為機器人數，L為指令總長
空間複雜度：O(S)，其中S為scent標記數
"""


def solve_robot_simulation():
    """
    主函數：讀取輸入並模擬機器人移動。
    """
    try:
        # 讀取網格邊界
        line = input().strip()
        if not line:
            return

        x_max, y_max = map(int, line.split())

        # 方向向量：北(0), 東(1), 南(2), 西(3)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        direction_names = ["N", "E", "S", "W"]

        # 存儲掉落位置（scent）
        scents = set()

        while True:
            try:
                # 讀取機器人初始位置和方向
                position_line = input().strip()
                if not position_line:
                    continue

                parts = position_line.split()
                x, y = int(parts[0]), int(parts[1])
                direction_char = parts[2]

                # 獲取初始方向索引
                direction_idx = direction_names.index(direction_char)

                # 讀取指令
                commands = input().strip()

                # 執行指令
                for cmd in commands:
                    if cmd == "L":
                        # 左轉：逆時針
                        direction_idx = (direction_idx - 1) % 4
                    elif cmd == "R":
                        # 右轉：順時針
                        direction_idx = (direction_idx + 1) % 4
                    elif cmd == "F":
                        # 前進
                        dx, dy = directions[direction_idx]
                        new_x, new_y = x + dx, y + dy

                        # 檢查是否超出邊界
                        if new_x < 0 or new_x > x_max or new_y < 0 or new_y > y_max:
                            # 檢查是否有scent標記
                            if (x, y) not in scents:
                                # 留下scent標記並輸出LOST
                                scents.add((x, y))
                                print(f"{x} {y} {direction_names[direction_idx]} LOST")
                                break
                            # 否則忽略此指令，機器人留在原地
                        else:
                            # 正常移動
                            x, y = new_x, new_y
                else:
                    # 所有指令執行完畢，機器人未掉落
                    print(f"{x} {y} {direction_names[direction_idx]}")

            except EOFError:
                break

    except EOFError:
        pass


if __name__ == "__main__":
    solve_robot_simulation()
