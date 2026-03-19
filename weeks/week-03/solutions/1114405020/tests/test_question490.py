#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 490 - 文本旋轉 測試程式
"""

import unittest


def rotate_text(lines):
    """旋轉文本90度"""
    if not lines:
        return []

    max_width = max(len(line) for line in lines)
    lines = [line.ljust(max_width) for line in lines]

    result = []
    for col in range(max_width - 1, -1, -1):
        result.append("".join(lines[row][col] for row in range(len(lines))))

    return result


class TestQuestion490(unittest.TestCase):
    def test_single_line(self):
        """測試：單行"""
        result = rotate_text(["ABC"])
        expected = ["C", "B", "A"]
        self.assertEqual(result, expected)

    def test_two_lines(self):
        """測試：兩行"""
        result = rotate_text(["AB", "CD"])
        expected = ["BD", "AC"]
        self.assertEqual(result, expected)

    def test_square(self):
        """測試：正方形"""
        result = rotate_text(["AB", "CD"])
        expected = ["BD", "AC"]
        self.assertEqual(result, expected)

    def test_empty(self):
        """測試：空列表"""
        result = rotate_text([])
        expected = []
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
