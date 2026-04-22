#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
題目 10268: 水球測試問題（二分搜尋 + 動態規劃）
單元測試文件

題目敘述：
有 k 個水球和 n 層樓（n 可能非常大，64 位元整數）。
需要找到水球會破裂的臨界樓層，最少需要測試幾次（最糟情況）。

測試用例覆蓋：
- 單個水球（必須逐層測試）
- 多個水球（可以二分搜尋）
- 大樓層數
- 邊界情況
"""

import unittest


class Solution10268:
    """
    解決 UVA 10268 問題的主要類別
    
    關鍵洞察：
    - 用 k 個水球測試 n 層樓，最少需要 t 次測試
    - 可以用 DP 思想：T(k, t) = 最多能測試的樓層數
    - T(k, t) = T(k-1, t-1) + T(k, t-1) + 1
      （當前層破 -> T(k-1, t-1)；未破 -> T(k, t-1)；當前層 -> 1）
    """
    
    def __init__(self):
        """初始化解決方案"""
        self.k = 0  # 水球數量
        self.n = 0  # 樓層數
        self.result = 0
    
    def solve(self, k, n):
        """
        找出最少需要的測試次數
        
        Args:
            k: 水球數量 (1 <= k <= 100)
            n: 樓層數 (64 位元整數)
        
        Returns:
            最少需要的測試次數，或 "More than 63 trials needed."
        """
        self.k = k
        self.n = n
        
        # 使用 DP：dp[t][j] = 用 j 個水球測試 t 次最多能確定的樓層數
        # 初始化
        max_trials = 64  # 題目要求 > 63 就輸出特殊信息
        
        # dp[t][j] = 用 j 個水球測試 t 次能判斷的最大樓層數
        dp = [[0] * (k + 1) for _ in range(max_trials)]
        
        # 基礎情況
        for j in range(k + 1):
            dp[0][j] = 0  # 0 次測試無法判斷任何樓層
        
        for t in range(1, max_trials):
            dp[t][0] = 0  # 沒有水球無法測試
            for j in range(1, k + 1):
                # 遞迴關係：
                # - 水球破：可以確定下面的 dp[t-1][j-1] 層
                # - 當前層：1 層
                # - 水球未破：可以確定上面的 dp[t-1][j] 層
                dp[t][j] = dp[t-1][j-1] + 1 + dp[t-1][j]
                
                # 如果已經能涵蓋 n 層，提前返回
                if dp[t][j] >= n:
                    return t
        
        # 如果 64 次測試都不夠
        return "More than 63 trials needed."
    
    def read_input(self, test_cases):
        """
        讀取多筆測試案例
        
        Args:
            test_cases: 測試案例列表，每個案例 (k, n)
        """
        results = []
        
        for k, n in test_cases:
            if k == 0:
                break
            
            result = self.solve(k, n)
            results.append((k, n, result))
            print(f"k={k}, n={n}: {result}")
        
        return results


class TestSolution10268(unittest.TestCase):
    """
    測試案例：驗證水球測試計算的正確性
    """
    
    def setUp(self):
        """設置測試環境"""
        self.solution = Solution10268()
    
    def test_single_ball_small_building(self):
        """測試：1 個水球，5 層樓"""
        result = self.solution.solve(1, 5)
        # 用 1 個水球只能逐層測試，所以需要 5 次
        self.assertEqual(result, 5)
    
    def test_single_ball_large_building(self):
        """測試：1 個水球，100 層樓"""
        result = self.solution.solve(1, 100)
        # 用 1 個水球需要 100 次，但超過 63 次上限會返回特殊字符串
        if isinstance(result, str):
            self.assertTrue("More than" in result)
        else:
            self.assertGreater(result, 63)
    
    def test_two_balls_small_building(self):
        """測試：2 個水球，10 層樓"""
        result = self.solution.solve(2, 10)
        # 用 2 個水球測試 10 層樓，最少 4 次
        # T(2, 1) = 2（層）
        # T(2, 2) = 1 + 1 + 2 = 4（層）
        # T(2, 3) = 1 + 3 + 4 = 8（層）
        # T(2, 4) = 1 + 7 + 8 = 16（層）> 10
        self.assertEqual(result, 4)
    
    def test_many_balls_large_building(self):
        """測試：100 個水球，大樓層數"""
        result = self.solution.solve(100, 10**18)
        # 有足夠的水球，可以用二分搜尋
        # 64 位元最多需要 64 次（二分）
        if isinstance(result, str):
            self.assertTrue(result.startswith("More than"))
        else:
            self.assertLessEqual(result, 64)
    
    def test_result_never_negative(self):
        """測試：結果永遠非負"""
        for k in [1, 2, 5, 10]:
            for n in [1, 10, 100]:
                result = self.solution.solve(k, n)
                if isinstance(result, int):
                    self.assertGreater(result, 0)
    
    def test_more_balls_faster(self):
        """測試：水球越多，測試次數越少"""
        result1 = self.solution.solve(1, 100)
        result2 = self.solution.solve(2, 100)
        result3 = self.solution.solve(5, 100)
        
        # 轉換為數字進行比較
        r1 = result1 if isinstance(result1, int) else 64
        r2 = result2 if isinstance(result2, int) else 64
        r3 = result3 if isinstance(result3, int) else 64
        
        self.assertGreater(r1, r2)
        self.assertGreater(r2, r3)
    
    def test_edge_case_one_floor(self):
        """測試：1 層樓"""
        result = self.solution.solve(2, 1)
        # 1 層樓只需 1 次測試
        self.assertEqual(result, 1)


def run_tests():
    """運行所有測試並生成報告"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSolution10268)
    
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
            (1, 10),
            (2, 100),
            (2, 10**9),
            (10, 10**18),
        ]
        
        solution = Solution10268()
        solution.read_input(test_cases)
