#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 118 - 機器人模擬 測試程式
"""

import unittest


class RobotSimulator:
    def __init__(self, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.scents = set()

    def simulate(self, x, y, direction_char, commands):
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


class TestQuestion118(unittest.TestCase):
    def test_simple_forward(self):
        """測試：簡單前進"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(0, 0, "N", "F")
        self.assertEqual(result, (0, 1, "N", None))

    def test_turn_left(self):
        """測試：左轉"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(2, 2, "N", "L")
        self.assertEqual(result, (2, 2, "W", None))

    def test_turn_right(self):
        """測試：右轉"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(2, 2, "N", "R")
        self.assertEqual(result, (2, 2, "E", None))

    def test_lost_north(self):
        """測試：向北掉落"""
        sim = RobotSimulator(5, 5)
        result = sim.simulate(2, 5, "N", "F")
        self.assertEqual(result, (2, 5, "N", "LOST"))

    def test_scent_marker(self):
        """測試：scent標記"""
        sim = RobotSimulator(3, 3)
        result1 = sim.simulate(3, 3, "N", "F")
        self.assertEqual(result1, (3, 3, "N", "LOST"))

        result2 = sim.simulate(3, 3, "N", "F")
        self.assertEqual(result2, (3, 3, "N", None))


if __name__ == "__main__":
    unittest.main(verbosity=2)
