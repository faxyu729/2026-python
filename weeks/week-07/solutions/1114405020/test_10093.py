#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 10093 - 炮兵部隊部署問題 單元測試程序

本程序包含6個測試用例，測試炮兵部隊最大部署數量的計算。
每個測試用例包含詳細的註釋說明其預期行為。

測試環境：Python 3.x
執行方式：python test_10093.py
"""

import unittest
from solution_10093 import solve_artillery


class TestArtilleryPlacement(unittest.TestCase):
    """
    炮兵部隊部署問題的單元測試類別。

    測試範圍包括：
    - 基本情況：小規模網格（3x3, 4x4）
    - 邊界情況：單行、單列網格
    - 特殊情況：全山地、全平原、混合地形
    """

    def test_case_1_3x3_all_plains(self):
        """
        測試用例 1: 3x3 全平原

        地圖：
        P P P
        P P P
        P P P

        預期輸出：3

        說明：
        在 3x3 全平原的網格中，由於炮兵攻擊範圍是
        橫向左右各2格、縱向上下各2格，最多能部署3支炮兵。
        例如可以在 (0,0)、(1,2)、(2,1) 放置。
        """
        n, m = 3, 3
        grid = ["PPP", "PPP", "PPP"]
        result = solve_artillery(n, m, grid)
        self.assertEqual(result, 3, "3x3全平原應最多部署3支炮兵")

    def test_case_2_4x4_all_plains(self):
        """
        測試用例 2: 4x4 全平原

        地圖：
        P P P P
        P P P P
        P P P P
        P P P P

        預期輸出：6

        說明：
        在 4x4 全平原的網格中，最多能部署6支炮兵。
        由於攻擊範圍限制，可以採用交錯放置的方式
        來最大化炮兵數量。
        """
        n, m = 4, 4
        grid = ["PPPP", "PPPP", "PPPP", "PPPP"]
        result = solve_artillery(n, m, grid)
        self.assertEqual(result, 6, "4x4全平原應最多部署6支炮兵")

    def test_case_3_1x1_single_plain(self):
        """
        測試用例 3: 1x1 單格平原

        地圖：
        P

        預期輸出：1

        說明：
        只有一格平原，直接部署1支炮兵。
        """
        n, m = 1, 1
        grid = ["P"]
        result = solve_artillery(n, m, grid)
        self.assertEqual(result, 1, "1x1單格應部署1支炮兵")

    def test_case_4_all_mountains(self):
        """
        測試用例 4: 3x3 全山地

        地圖：
        H H H
        H H H
        H H H

        預期輸出：0

        說明：
        全是山地，無法部署任何炮兵。
        """
        n, m = 3, 3
        grid = ["HHH", "HHH", "HHH"]
        result = solve_artillery(n, m, grid)
        self.assertEqual(result, 0, "全山地應部署0支炮兵")

    def test_case_5_mixed_terrain(self):
        """
        測試用例 5: 5x3 混合地形

        地圖：
        P H P
        H P H
        P P P
        H P H
        P H P

        預期輸出：4

        說明：
        混合地形的複雜情況，需要動態規劃來計算
        最大部署數量。
        """
        n, m = 5, 3
        grid = ["PHP", "HPH", "PPP", "HPH", "PHP"]
        result = solve_artillery(n, m, grid)
        self.assertEqual(result, 4, "5x3混合地形應最多部署4支炮兵")

    def test_case_6_single_row(self):
        """
        測試用例 6: 1x5 單行平原

        地圖：
        P P P P P

        預期輸出：2

        說明：
        單行的情況下，由於橫向攻擊範圍是左右各2格，
        最多能部署2支炮兵。
        """
        n, m = 5, 1
        grid = ["P", "P", "P", "P", "P"]
        result = solve_artillery(n, m, grid)
        self.assertEqual(result, 2, "5x1單列應最多部署2支炮兵")


class TestArtilleryHelperFunctions(unittest.TestCase):
    """
    輔助函數的單元測試類別。

    測試是否能正確判斷兩個炮兵位置是否會互相攻擊。
    """

    def test_attack_range_horizontal(self):
        """
        測試水平攻擊範圍判定。

        說明：炮兵在 (row, col) 的水平攻擊範圍應該是
        同一行的 [col-2, col+2] 範圍內（除了自己所在位置）。
        距離≤2表示在攻擊範圍內。
        """
        from solution_10093 import can_place_artillery

        # 在 (0, 0) 和 (0, 3) 放置 - 應該能放（距離為3，超出範圍）
        n, m = 1, 5
        grid = ["PPPPP"]
        placements = [(0, 0), (0, 3)]
        result = can_place_artillery(n, m, grid, placements)
        # 距離為3，超出攻擊範圍，應能放置
        self.assertTrue(result, "(0,0)和(0,3)應能同時放置")

    def test_attack_range_vertical(self):
        """
        測試垂直攻擊範圍判定。

        說明：炮兵在 (row, col) 的垂直攻擊範圍應該是
        同一列的 [row-2, row+2] 範圍內（除了自己所在位置）。
        距離≤2表示在攻擊範圍內。
        """
        from solution_10093 import can_place_artillery

        # 在 (0, 0) 和 (3, 0) 放置 - 應該能放（距離為3，超出範圍）
        n, m = 5, 1
        grid = ["P", "P", "P", "P", "P"]
        placements = [(0, 0), (3, 0)]
        result = can_place_artillery(n, m, grid, placements)
        # 距離為3，超出攻擊範圍，應能放置
        self.assertTrue(result, "(0,0)和(3,0)應能同時放置")


if __name__ == "__main__":
    # 執行所有測試並輸出詳細結果
    unittest.main(verbosity=2)
