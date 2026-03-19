#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 118 - 機器人模擬 (Robot Simulation) 測試檔

測試機器人的四個基本操作：
1. 左轉（L）：逆時針旋轉90度
2. 右轉（R）：順時針旋轉90度
3. 前進（F）：沿著面向方向移動一格
4. 掉落並留下標記（LOST）
"""

import unittest
from io import StringIO
import sys


class RobotSimulator:
    """機器人模擬類"""

    def __init__(self, x_max, y_max):
        """
        初始化機器人模擬環境。

        參數：
            x_max (int)：網格右邊界座標
            y_max (int)：網格上邊界座標
        """
        self.x_max = x_max
        self.y_max = y_max
        self.scents = set()  # 掉落位置的標記

    def simulate(self, x, y, direction_char, commands):
        """
        模擬單個機器人的移動。

        參數：
            x (int)：初始x座標
            y (int)：初始y座標
            direction_char (str)：初始方向('N', 'S', 'E', 'W')
            commands (str)：指令字串('L', 'R', 'F')

        返回：
            tuple：最終位置和方向，或(x, y, direction, "LOST")
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        direction_names = ["N", "E", "S", "W"]

        direction_idx = direction_names.index(direction_char)

        for cmd in commands:
            if cmd == "L":
                direction_idx = (direction_idx - 1) % 4
            elif cmd == "R":
                direction_idx = (direction_idx + 1) % 4
            elif cmd == "F":
                dx, dy = directions[direction_idx]
                new_x, new_y = x + dx, y + dy

                if new_x < 0 or new_x > self.x_max or new_y < 0 or new_y > self.y_max:
                    if (x, y) not in self.scents:
                        self.scents.add((x, y))
                        return (x, y, direction_names[direction_idx], "LOST")
                else:
                    x, y = new_x, new_y

        return (x, y, direction_names[direction_idx], None)


class TestRobotSimulation(unittest.TestCase):
    """機器人模擬測試類"""

    def test_simple_forward(self):
        """測試：簡單前進"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(0, 0, "N", "F")
        self.assertEqual(result, (0, 1, "N", None))

    def test_turn_left(self):
        """測試：左轉不改變位置"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(2, 2, "N", "L")
        self.assertEqual(result, (2, 2, "W", None))

    def test_turn_right(self):
        """測試：右轉不改變位置"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(2, 2, "N", "R")
        self.assertEqual(result, (2, 2, "E", None))

    def test_complete_rotation(self):
        """測試：完整旋轉回到原方向"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(2, 2, "N", "RRRR")
        self.assertEqual(result, (2, 2, "N", None))

    def test_all_directions(self):
        """測試：四個方向的前進"""
        sim = RobotSimulator(10, 10)

        # 向北
        result = sim.simulate(5, 5, "N", "F")
        self.assertEqual(result[0:3], (5, 6, "N"))

        # 向東
        sim = RobotSimulator(10, 10)
        result = sim.simulate(5, 5, "E", "F")
        self.assertEqual(result[0:3], (6, 5, "E"))

        # 向南
        sim = RobotSimulator(10, 10)
        result = sim.simulate(5, 5, "S", "F")
        self.assertEqual(result[0:3], (5, 4, "S"))

        # 向西
        sim = RobotSimulator(10, 10)
        result = sim.simulate(5, 5, "W", "F")
        self.assertEqual(result[0:3], (4, 5, "W"))

    def test_lost_north(self):
        """測試：向北掉落"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(2, 5, "N", "F")
        self.assertEqual(result, (2, 5, "N", "LOST"))

    def test_lost_east(self):
        """測試：向東掉落"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(5, 2, "E", "F")
        self.assertEqual(result, (5, 2, "E", "LOST"))

    def test_lost_south(self):
        """測試：向南掉落"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(2, 0, "S", "F")
        self.assertEqual(result, (2, 0, "S", "LOST"))

    def test_lost_west(self):
        """測試：向西掉落"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(0, 2, "W", "F")
        self.assertEqual(result, (0, 2, "W", "LOST"))

    def test_scent_marker(self):
        """測試：scent標記防止再次掉落"""
        sim = RobotSimulator(3, 3)

        # 第一個機器人掉落並留下標記
        result1 = sim.simulate(3, 3, "N", "F")
        self.assertEqual(result1, (3, 3, "N", "LOST"))

        # 第二個機器人在同一位置被scent標記阻擋
        result2 = sim.simulate(3, 3, "N", "F")
        self.assertEqual(result2, (3, 3, "N", None))

    def test_complex_sequence(self):
        """測試：複雜指令序列"""
        sim = RobotSimulator(5, 5)
        # 從(0,0)向北，前進、右轉、前進
        result = sim.simulate(0, 0, "N", "FRF")
        self.assertEqual(result, (1, 1, "E", None))


if __name__ == "__main__":
    unittest.main(verbosity=2)
