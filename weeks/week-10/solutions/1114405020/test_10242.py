#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
題目 10242: ATM 搶劫（圖論 + 動態規劃）
單元測試文件

題目敘述：
在有向圖中，從起點出發，可多次經過同一邊，但每個 ATM 只能搶一次。
要求找到到達某個酒吧時，能搶到的最多現金。

測試用例覆蓋：
- 簡單的線性圖
- 環形圖
- 多條路徑
- 無法到達酒吧的情況
"""

import unittest
from collections import defaultdict, deque


class Solution10242:
    """
    解決 UVA 10242 問題的主要類別
    
    使用圖論和狀態空間搜索（BFS/DFS）來找到最大搶劫金額。
    """
    
    def __init__(self):
        """初始化解決方案"""
        self.n = 0  # 路口數
        self.m = 0  # 道路數
        self.graph = defaultdict(list)  # graph[u] = [(v, ...)]
        self.atm_values = []  # 每個路口的 ATM 金額
        self.start = 0  # 起點路口
        self.bars = set()  # 有酒吧的路口集合
        self.max_money = 0  # 最大搶劫金額
    
    def read_input(self):
        """讀取圖的輸入資料"""
        self.n, self.m = map(int, input().split())
        
        self.graph = defaultdict(list)
        
        # 讀取道路
        for _ in range(self.m):
            u, v = map(int, input().split())
            u -= 1  # 轉換為 0-based
            v -= 1
            self.graph[u].append(v)
        
        # 讀取 ATM 金額
        self.atm_values = []
        for _ in range(self.n):
            value = int(input())
            self.atm_values.append(value)
        
        # 讀取起點和酒吧
        self.start, p = map(int, input().split())
        self.start -= 1  # 轉換為 0-based
        
        self.bars = set()
        bar_ids = list(map(int, input().split()))
        for bar_id in bar_ids:
            self.bars.add(bar_id - 1)  # 轉換為 0-based
        
        return self.solve()
    
    def solve(self):
        """
        使用 BFS 和動態規劃搜索最大搶劫金額
        
        狀態：(當前位置, 已搶劫的 ATM 集合)
        
        Returns:
            最大搶劫金額
        """
        from collections import deque
        
        # 使用 BFS 探索所有可能的狀態
        # 最多搶劫所有 ATM 的不同子集有限
        max_money = 0
        visited = set()
        
        # 初始狀態：在起點，已搶劫起點的 ATM
        initial_state = (self.start, frozenset([self.start]))
        queue = deque([initial_state])
        visited.add(initial_state)
        
        iteration_limit = 10000  # 限制迭代次數以防止無限循環
        count = 0
        
        while queue and count < iteration_limit:
            count += 1
            node, robbed = queue.popleft()
            
            # 檢查是否到達酒吧
            if node in self.bars:
                current_money = sum(self.atm_values[atm] for atm in robbed)
                max_money = max(max_money, current_money)
            
            # 探索相鄰節點
            for next_node in self.graph[node]:
                new_robbed = robbed
                
                # 如果下一個節點有 ATM 且未被搶過
                if next_node not in robbed and next_node < len(self.atm_values):
                    new_robbed = robbed | frozenset([next_node])
                
                new_state = (next_node, new_robbed)
                
                # 避免重複訪問相同狀態
                if new_state not in visited and len(visited) < 50000:
                    visited.add(new_state)
                    queue.append(new_state)
        
        return max_money


class TestSolution10242(unittest.TestCase):
    """
    測試案例：驗證 ATM 搶劫計算的正確性
    """
    
    def setUp(self):
        """設置測試環境"""
        self.solution = Solution10242()
    
    def test_single_node_with_bar(self):
        """測試：單一節點同時是起點和酒吧"""
        solution = Solution10242()
        solution.n = 1
        solution.m = 0
        solution.graph = defaultdict(list)
        solution.atm_values = [100]
        solution.start = 0
        solution.bars = {0}
        
        result = solution.solve()
        # 起點有 100 元，起點就是酒吧，所以結果是 100
        self.assertEqual(result, 100)
    
    def test_linear_path(self):
        """測試：線性路徑 1->2->3"""
        solution = Solution10242()
        solution.n = 3
        solution.m = 2
        solution.graph = defaultdict(list, {
            0: [1],
            1: [2],
        })
        solution.atm_values = [10, 20, 30]
        solution.start = 0
        solution.bars = {2}  # 只有節點 3 有酒吧
        
        result = solution.solve()
        # 路徑：1(10) -> 2(20) -> 3(30)，總共 60
        self.assertEqual(result, 60)
    
    def test_no_bar_reachable(self):
        """測試：無法到達酒吧"""
        solution = Solution10242()
        solution.n = 3
        solution.m = 1
        solution.graph = defaultdict(list, {
            0: [1],
        })
        solution.atm_values = [10, 20, 30]
        solution.start = 0
        solution.bars = {2}  # 無法從節點 1 到達節點 3
        
        result = solution.solve()
        # 無法到達酒吧，結果應為 0
        self.assertEqual(result, 0)
    
    def test_cycle_with_bar(self):
        """測試：環形圖"""
        solution = Solution10242()
        solution.n = 3
        solution.m = 3
        solution.graph = defaultdict(list, {
            0: [1],
            1: [2],
            2: [0],  # 形成環
        })
        solution.atm_values = [10, 20, 30]
        solution.start = 0
        solution.bars = {1}
        
        result = solution.solve()
        # 可以繞一圈回到節點 2，所以可以搶更多 ATM
        self.assertGreater(result, 0)


def run_tests():
    """運行所有測試並生成報告"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSolution10242)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
