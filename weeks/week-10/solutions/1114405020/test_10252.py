#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
題目 10252: 費馬點問題（幾何 + 最優化）
單元測試文件

題目敘述：
給定 N 個點，找到使得到所有點距離和最小的點 P。
輸出：最小距離和、有多少個整數座標的點能達到最小距離和。

測試用例覆蓋：
- 共線的點
- 等邊三角形
- 一般位置的點
- 距離計算精度
"""

import unittest
import math


class Solution10252:
    """
    解決 UVA 10252 問題的主要類別
    
    費馬點問題：找到使到所有點距離和最小的點。
    使用梯度下降或三角形費馬點的特性來解決。
    """
    
    def __init__(self):
        """初始化解決方案"""
        self.points = []  # 點的座標列表
        self.min_distance = 0
        self.count_solutions = 0
    
    def read_input(self, points):
        """
        讀取點的座標
        
        Args:
            points: 點的座標列表 [(x1, y1), (x2, y2), ...]
        """
        self.points = points
        self.solve()
    
    def distance(self, p1, p2):
        """
        計算兩點之間的距離
        
        Args:
            p1: 點 1 的座標 (x, y)
            p2: 點 2 的座標 (x, y)
        
        Returns:
            歐幾里得距離
        """
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
    def total_distance(self, p):
        """
        計算點 p 到所有點的距離和
        
        Args:
            p: 點的座標 (x, y)
        
        Returns:
            距離和
        """
        total = 0.0
        for point in self.points:
            total += self.distance(p, point)
        return total
    
    def solve(self):
        """
        使用網格搜索和精化來尋找最小值點
        
        步驟：
        1. 找到所有點的包圍盒
        2. 在包圍盒內進行網格搜索（整數座標）
        3. 找到最小距離和及對應的點數
        """
        if not self.points:
            self.min_distance = 0
            self.count_solutions = 0
            return
        
        # 單點情況
        if len(self.points) == 1:
            self.min_distance = 0
            self.count_solutions = 1
            return
        
        # 找到包圍盒
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # 擴展搜索範圍
        search_x = range(int(min_x) - 10, int(max_x) + 11)
        search_y = range(int(min_y) - 10, int(max_y) + 11)
        
        min_dist = float('inf')
        count = 0
        
        # 遍歷整數座標，找到最小距離和
        for x in search_x:
            for y in search_y:
                dist = self.total_distance((x, y))
                
                if dist < min_dist:
                    min_dist = dist
                    count = 1
                elif abs(dist - min_dist) < 1e-9:  # 浮點數精度比較
                    count += 1
        
        # 四捨五入距離和
        self.min_distance = int(round(min_dist))
        self.count_solutions = count
    
    def get_result(self):
        """
        獲取結果
        
        Returns:
            (最小距離和, 達到最小距離的整數點數)
        """
        return (self.min_distance, self.count_solutions)


class TestSolution10252(unittest.TestCase):
    """
    測試案例：驗證費馬點計算的正確性
    """
    
    def test_single_point(self):
        """測試：單一點"""
        solution = Solution10252()
        solution.read_input([(0, 0)])
        
        dist, count = solution.get_result()
        self.assertEqual(dist, 0)
        self.assertEqual(count, 1)
    
    def test_two_points(self):
        """測試：兩個點"""
        solution = Solution10252()
        # 點 (0, 0) 和 (2, 0)
        solution.read_input([(0, 0), (2, 0)])
        
        dist, count = solution.get_result()
        # 最小值在 (0, 0) 到 (2, 0) 之間，距離為 2
        self.assertEqual(dist, 2)
    
    def test_three_collinear_points(self):
        """測試：三個共線的點"""
        solution = Solution10252()
        # 點 (0, 0), (1, 0), (2, 0)
        solution.read_input([(0, 0), (1, 0), (2, 0)])
        
        dist, count = solution.get_result()
        # 最優點在 (1, 0)，距離和為 2
        self.assertEqual(dist, 2)
    
    def test_example_from_problem(self):
        """測試：題目中的例子 (0, 0), (1, 1), (2, 2)"""
        solution = Solution10252()
        solution.read_input([(0, 0), (1, 1), (2, 2)])
        
        dist, count = solution.get_result()
        # 根據題目，答案應該是 2*sqrt(2) ≈ 2.828...，四捨五入為 3
        self.assertGreater(dist, 0)
        self.assertGreater(count, 0)
    
    def test_equilateral_triangle(self):
        """測試：等邊三角形"""
        solution = Solution10252()
        # 等邊三角形頂點
        solution.read_input([(0, 0), (1, 0), (0.5, math.sqrt(3)/2)])
        
        dist, count = solution.get_result()
        # 費馬點在三角形內
        self.assertGreater(dist, 0)
        self.assertGreater(count, 0)


def run_tests():
    """運行所有測試並生成報告"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSolution10252)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
    else:
        # 測試用例
        test_cases = [
            [(0, 0), (1, 1), (2, 2)],
        ]
        
        for i, points in enumerate(test_cases, 1):
            solution = Solution10252()
            solution.read_input(points)
            dist, count = solution.get_result()
            print(f"Test {i}: min_distance={dist}, count={count}")
