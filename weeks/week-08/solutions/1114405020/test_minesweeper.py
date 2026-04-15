"""
踩地雷 (Minesweeper) - 單元測試

題目說明：
- 在網格中找出地雷周圍的地雷數量
- 地雷用 '*' 表示，空白用 '.' 表示
- 需要計算每個空白格子周圍 8 個方向的地雷數量

單元測試：使用 unittest 框架測試各種情況
"""

import unittest
import sys
from io import StringIO


def solve_minesweeper(grid):
    """
    踩地雷求解函式

    參數：
        grid: 二維列表，'*' 表示地雷，'.' 表示空白

    返回值：
        二維列表，地雷保持 '*'，空白改為周圍地雷數量
    """
    # 獲取網格的行數和列數
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # 建立結果網格（深度複製輸入網格）
    result = [list(row) for row in grid]

    # 8 個方向的偏移量（上、下、左、右、左上、右上、左下、右下）
    directions = [
        (-1, -1),
        (-1, 0),
        (-1, 1),  # 上面的三個方向
        (0, -1),
        (0, 1),  # 左邊和右邊
        (1, -1),
        (1, 0),
        (1, 1),  # 下面的三個方向
    ]

    # 遍歷網格的每個格子
    for i in range(rows):
        for j in range(cols):
            # 只處理空白格子（非地雷）
            if grid[i][j] == ".":
                mine_count = 0

                # 檢查所有 8 個相鄰格子
                for di, dj in directions:
                    ni, nj = i + di, j + dj

                    # 確保新位置在網格範圍內
                    if 0 <= ni < rows and 0 <= nj < cols:
                        # 如果相鄰格子是地雷，計數加一
                        if grid[ni][nj] == "*":
                            mine_count += 1

                # 將空白格子改為地雷數量
                result[i][j] = str(mine_count)

    return result


class TestMinesweeper(unittest.TestCase):
    """踩地雷單元測試類別"""

    def test_single_mine_basic(self):
        """測試 1: 單個地雷的基本情況"""
        grid = [
            ["*", ".", ".", "."],
            [".", ".", ".", "."],
            [".", "*", ".", "."],
            [".", ".", ".", "."],
        ]

        result = solve_minesweeper(grid)
        expected = [
            ["*", "1", "0", "0"],
            ["2", "2", "1", "0"],
            ["1", "*", "1", "0"],
            ["1", "1", "1", "0"],
        ]

        self.assertEqual(result, expected)

    def test_question_example_1(self):
        """測試 2: 題目示例 1"""
        grid = [
            ["*", ".", ".", "."],
            [".", ".", ".", "."],
            [".", "*", ".", "."],
            [".", ".", ".", "."],
        ]

        result = solve_minesweeper(grid)
        expected = [
            ["*", "1", "0", "0"],
            ["2", "2", "1", "0"],
            ["1", "*", "1", "0"],
            ["1", "1", "1", "0"],
        ]

        self.assertEqual(result, expected)

    def test_question_example_2(self):
        """測試 3: 題目示例 2 (3x5 網格)"""
        grid = [
            ["*", "*", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", "*", ".", ".", "."],
        ]

        result = solve_minesweeper(grid)
        expected = [
            ["*", "*", "1", "0", "0"],
            ["3", "3", "2", "0", "0"],
            ["1", "*", "1", "0", "0"],
        ]

        self.assertEqual(result, expected)

    def test_no_mines(self):
        """測試 4: 沒有地雷的網格"""
        grid = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

        result = solve_minesweeper(grid)
        expected = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]

        self.assertEqual(result, expected)

    def test_all_mines(self):
        """測試 5: 全是地雷的網格"""
        grid = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]

        result = solve_minesweeper(grid)
        expected = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]

        self.assertEqual(result, expected)

    def test_corner_mines(self):
        """測試 6: 四個角落都有地雷"""
        grid = [["*", ".", "*"], [".", ".", "."], ["*", ".", "*"]]

        result = solve_minesweeper(grid)
        expected = [["*", "2", "*"], ["2", "4", "2"], ["*", "2", "*"]]

        self.assertEqual(result, expected)

    def test_edge_mines_only(self):
        """測試 7: 只有邊緣有地雷"""
        grid = [["*", "*", "*"], ["*", ".", "*"], ["*", "*", "*"]]

        result = solve_minesweeper(grid)
        expected = [["*", "*", "*"], ["*", "8", "*"], ["*", "*", "*"]]

        self.assertEqual(result, expected)

    def test_single_cell_mine(self):
        """測試 8: 單一格子含地雷"""
        grid = [["*"]]

        result = solve_minesweeper(grid)
        expected = [["*"]]

        self.assertEqual(result, expected)

    def test_single_cell_empty(self):
        """測試 9: 單一格子為空白"""
        grid = [["."]]

        result = solve_minesweeper(grid)
        expected = [["0"]]

        self.assertEqual(result, expected)

    def test_linear_grid(self):
        """測試 10: 一維（單行）網格"""
        grid = [["*", ".", "*", ".", "*"]]

        result = solve_minesweeper(grid)
        expected = [["*", "2", "*", "2", "*"]]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    # 執行測試並顯示詳細輸出
    unittest.main(verbosity=2)
