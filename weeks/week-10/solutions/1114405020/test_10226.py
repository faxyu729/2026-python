#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
題目 10226: 排列問題（DFS + 剪枝）
單元測試文件

題目敘述：
給定 N 個人（編號 A, B, ..., Z），每個人有不想排的位置限制。
輸出所有可能的排列（按字典序），相同的前綴部分不重複輸出。

測試用例覆蓋：
- 基礎排列功能
- 位置限制的處理
- 字典序排列
- 前綴優化輸出
"""

import unittest
from io import StringIO
import sys


class Solution10226:
    """
    解決 UVA 10226 問題的主要類別
    
    使用 DFS 回溯法生成所有有效排列，
    根據位置限制進行剪枝優化。
    """
    
    def __init__(self):
        """初始化排列生成器"""
        self.n = 0
        self.forbidden = {}  # forbidden[i] = set of forbidden positions for person i
        self.permutations = []  # 存儲所有有效排列
    
    def read_input(self):
        """
        讀取輸入資料
        
        格式：
        N - 人數
        接下來 N 行，每行輸入第 i 個人不想排的位置（0 表示結束）
        """
        while True:
            try:
                n = int(input())
                if n == 0:
                    break
                
                self.n = n
                self.forbidden = {}
                self.permutations = []
                
                # 讀取每個人的限制
                for i in range(n):
                    forbidden_set = set()
                    while True:
                        pos = int(input())
                        if pos == 0:
                            break
                        # 轉換為 0-based 索引
                        forbidden_set.add(pos - 1)
                    
                    self.forbidden[i] = forbidden_set
                
                # 生成排列
                self.generate_permutations()
                self.print_permutations()
                
            except EOFError:
                break
    
    def generate_permutations(self):
        """
        使用 DFS 回溯法生成所有有效排列
        
        時間複雜度：O(N!)
        空間複雜度：O(N)
        """
        self.permutations = []
        used = [False] * self.n
        current = []
        
        def backtrack(pos):
            """
            回溯函數
            
            Args:
                pos: 當前要填充的位置（0-based）
            """
            if pos == self.n:
                # 找到一個有效排列
                self.permutations.append(current[:])
                return
            
            # 嘗試每個未使用的人
            for person in range(self.n):
                if used[person]:
                    continue
                
                # 檢查這個人是否可以排在當前位置
                if pos in self.forbidden[person]:
                    continue
                
                # 選擇
                used[person] = True
                current.append(person)
                
                # 遞迴
                backtrack(pos + 1)
                
                # 回溯
                current.pop()
                used[person] = False
        
        backtrack(0)
        # 排序確保字典序
        self.permutations.sort()
    
    def print_permutations(self):
        """
        打印排列，相同前綴不重複輸出
        
        優化：只輸出與前一個排列不同的部分
        """
        if not self.permutations:
            return
        
        prev = []
        for perm in self.permutations:
            # 找到不同的起始位置
            i = 0
            while i < len(prev) and i < len(perm) and prev[i] == perm[i]:
                i += 1
            
            # 輸出不同的部分
            output = ' '.join(chr(ord('A') + p) for p in perm[i:])
            print(output)
            prev = perm


class TestSolution10226(unittest.TestCase):
    """
    測試案例：驗證排列生成的正確性
    """
    
    def test_single_person(self):
        """測試：單一人物的排列"""
        solution = Solution10226()
        solution.n = 1
        solution.forbidden = {0: set()}
        solution.generate_permutations()
        
        # 只有一種排列：A
        self.assertEqual(len(solution.permutations), 1)
        self.assertEqual(solution.permutations[0], [0])
    
    def test_two_people_no_restrictions(self):
        """測試：兩人，無限制"""
        solution = Solution10226()
        solution.n = 2
        solution.forbidden = {0: set(), 1: set()}
        solution.generate_permutations()
        
        # 應有 2! = 2 種排列
        self.assertEqual(len(solution.permutations), 2)
        self.assertIn([0, 1], solution.permutations)  # AB
        self.assertIn([1, 0], solution.permutations)  # BA
    
    def test_two_people_with_restrictions(self):
        """測試：兩人，有位置限制"""
        solution = Solution10226()
        solution.n = 2
        # 人 0 不能在位置 1（0-based: 位置 0）
        # 人 1 不能在位置 2（0-based: 位置 1）
        solution.forbidden = {0: {0}, 1: {1}}
        solution.generate_permutations()
        
        # 只有排列 BA 滿足條件
        self.assertEqual(len(solution.permutations), 1)
        self.assertEqual(solution.permutations[0], [1, 0])
    
    def test_three_people_no_restrictions(self):
        """測試：三人，無限制"""
        solution = Solution10226()
        solution.n = 3
        solution.forbidden = {0: set(), 1: set(), 2: set()}
        solution.generate_permutations()
        
        # 應有 3! = 6 種排列
        self.assertEqual(len(solution.permutations), 6)
    
    def test_permutation_sorted(self):
        """測試：排列按字典序排列"""
        solution = Solution10226()
        solution.n = 3
        solution.forbidden = {0: set(), 1: set(), 2: set()}
        solution.generate_permutations()
        
        # 驗證排列已排序
        expected = sorted(solution.permutations)
        self.assertEqual(solution.permutations, expected)
    
    def test_complex_restrictions(self):
        """測試：複雜的位置限制"""
        solution = Solution10226()
        solution.n = 2
        # 人 0 不能在位置 1 和 2
        # 人 1 不能在位置 1
        solution.forbidden = {0: {0, 1}, 1: {0}}
        solution.generate_permutations()
        
        # 沒有有效排列
        self.assertEqual(len(solution.permutations), 0)


def run_tests():
    """運行所有測試並生成報告"""
    # 創建測試套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSolution10226)
    
    # 運行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回測試結果
    return result


if __name__ == '__main__':
    # 可以直接運行測試或交互式輸入
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # 運行單元測試
        run_tests()
    else:
        # 交互式模式（讀取輸入並處理）
        solution = Solution10226()
        try:
            solution.read_input()
        except EOFError:
            pass
