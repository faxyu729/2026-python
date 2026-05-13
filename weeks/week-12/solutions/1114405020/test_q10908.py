"""
UVA 10908 - Largest Square 單元測試

題目說明：
給定一個 M 行 N 列的字元網格，對於每個查詢點 (r, c)，
找出以該點為中心，所有字元相同的最大正方形的邊長。
正方形邊長必須為奇數（1, 3, 5, ...）
"""

import unittest


class TestQ10908(unittest.TestCase):
    """
    針對 UVA 10908 - Largest Square 的單元測試類別
    測試各種網格配置和查詢場景
    """
    
    def find_largest_square(self, grid, r, c):
        """
        在給定網格中，找出以 (r, c) 為中心的最大同字元正方形的邊長。
        
        參數：
            grid: 二維字元網格（列表的列表）
            r: 查詢點的行號（0 索引）
            c: 查詢點的列號（0 索引）
        
        返回：
            最大正方形的邊長（奇數）
        
        邏輯：
            1. 獲取中心點的字元
            2. 從邊長 1 開始，逐漸增加（每次增加 2，保證奇數）
            3. 對於每個邊長，檢查以 (r, c) 為中心的正方形內所有字元
            4. 當發現某個邊長不符合條件時，停止並返回前一個有效的邊長
        """
        # 獲取網格尺寸
        m = len(grid)
        n = len(grid[0]) if m > 0 else 0
        
        # 獲取中心點的字元
        center_char = grid[r][c]
        
        # 初始化最大邊長為 1
        max_length = 1
        
        # 計算最大可能的邊長（受邊界限制）
        # 距離上邊界 r 格、下邊界 (m-1-r) 格、左邊界 c 格、右邊界 (n-1-c) 格
        max_distance = min(r, c, m - 1 - r, n - 1 - c)
        max_possible = 2 * max_distance + 1
        
        # 嘗試所有可能的邊長（1, 3, 5, ...）
        for length in range(1, max_possible + 1, 2):
            # 計算距離中心的距離
            distance = length // 2
            
            # 標記正方形是否符合條件
            valid = True
            
            # 檢查以 (r, c) 為中心、邊長為 length 的正方形
            # 需要檢查的範圍：[r-distance, r+distance] × [c-distance, c+distance]
            for i in range(r - distance, r + distance + 1):
                for j in range(c - distance, c + distance + 1):
                    # 檢查是否超出邊界
                    if i < 0 or i >= m or j < 0 or j >= n:
                        valid = False
                        break
                    # 檢查字元是否與中心相同
                    if grid[i][j] != center_char:
                        valid = False
                        break
                if not valid:
                    break
            
            # 如果符合條件，記錄此邊長
            if valid:
                max_length = length
            else:
                # 如果當前邊長不符合，更大的邊長也不會符合
                break
        
        return max_length
    
    # ===== 基本測試用例 =====
    
    def test_single_cell(self):
        """
        測試最小情況：單個格子
        網格：1x1，只有一個字元
        查詢：(0, 0)
        預期：1（邊長為 1）
        """
        grid = ["a"]
        result = self.find_largest_square(grid, 0, 0)
        self.assertEqual(result, 1)
    
    def test_all_same_2x2(self):
        """
        測試 2x2 網格，所有字元相同
        網格：
        aa
        aa
        查詢：(0, 0)
        預期：1（邊長只能是 1，因為 2 是偶數）
        """
        grid = ["aa", "aa"]
        result = self.find_largest_square(grid, 0, 0)
        self.assertEqual(result, 1)
    
    def test_all_same_3x3(self):
        """
        測試 3x3 網格，所有字元相同
        網格：
        aaa
        aaa
        aaa
        查詢中心 (1, 1)：邊長應為 3
        """
        grid = ["aaa", "aaa", "aaa"]
        result = self.find_largest_square(grid, 1, 1)
        self.assertEqual(result, 3)
    
    def test_center_different(self):
        """
        測試中心點不同的情況
        網格：
        aaa
        aba
        aaa
        查詢中心 (1, 1) 的 'b'：邊長應為 1
        """
        grid = ["aaa", "aba", "aaa"]
        result = self.find_largest_square(grid, 1, 1)
        self.assertEqual(result, 1)
    
    # ===== 複雜情況測試 =====
    
    def test_official_example_case1(self):
        """
        測試官方範例中的第一個查詢
        網格（7x10）：
        abbbaaaaaa
        abbbaaaaaa
        abbbaaaaaa
        aaaaaaaaaa
        aaaaaaaaaa
        aaccaaaaaa
        aaccaaaaaa
        
        查詢 (1, 2)：中心字元是 'b'
        預期：3（邊長為 3 的 'b' 正方形）
        """
        grid = [
            "abbbaaaaaa",
            "abbbaaaaaa",
            "abbbaaaaaa",
            "aaaaaaaaaa",
            "aaaaaaaaaa",
            "aaccaaaaaa",
            "aaccaaaaaa"
        ]
        result = self.find_largest_square(grid, 1, 2)
        self.assertEqual(result, 3)
    
    def test_official_example_case2(self):
        """
        測試官方範例中的第二個查詢
        查詢 (2, 4)：中心字元是 'b'，但周圍有 'a'
        預期：1（只能是 1）
        """
        grid = [
            "abbbaaaaaa",
            "abbbaaaaaa",
            "abbbaaaaaa",
            "aaaaaaaaaa",
            "aaaaaaaaaa",
            "aaccaaaaaa",
            "aaccaaaaaa"
        ]
        result = self.find_largest_square(grid, 2, 4)
        self.assertEqual(result, 1)
    
    def test_official_example_case3(self):
        """
        測試官方範例中的第三個查詢
        查詢 (4, 6)：中心字元是 'a'
        預期：5（大型 'a' 正方形）
        """
        grid = [
            "abbbaaaaaa",
            "abbbaaaaaa",
            "abbbaaaaaa",
            "aaaaaaaaaa",
            "aaaaaaaaaa",
            "aaccaaaaaa",
            "aaccaaaaaa"
        ]
        result = self.find_largest_square(grid, 4, 6)
        self.assertEqual(result, 5)
    
    def test_official_example_case4(self):
        """
        測試官方範例中的第四個查詢
        查詢 (5, 2)：中心字元是 'c'
        預期：1（'c' 只有 2 個相鄰，無法形成更大的正方形）
        """
        grid = [
            "abbbaaaaaa",
            "abbbaaaaaa",
            "abbbaaaaaa",
            "aaaaaaaaaa",
            "aaaaaaaaaa",
            "aaccaaaaaa",
            "aaccaaaaaa"
        ]
        result = self.find_largest_square(grid, 5, 2)
        self.assertEqual(result, 1)
    
    # ===== 邊界測試 =====
    
    def test_corner_top_left(self):
        """
        測試左上角查詢
        網格：
        aaa
        aaa
        aaa
        查詢 (0, 0)：只能向右下擴展
        預期：1（因為只有 1 格可以向下和向右）
        """
        grid = ["aaa", "aaa", "aaa"]
        result = self.find_largest_square(grid, 0, 0)
        self.assertEqual(result, 1)
    
    def test_corner_top_right(self):
        """
        測試右上角查詢
        網格（3x3）：
        aaa
        aaa
        aaa
        查詢 (0, 2)：只能向左下擴展
        預期：1
        """
        grid = ["aaa", "aaa", "aaa"]
        result = self.find_largest_square(grid, 0, 2)
        self.assertEqual(result, 1)
    
    def test_corner_bottom_left(self):
        """
        測試左下角查詢
        網格（3x3）：
        aaa
        aaa
        aaa
        查詢 (2, 0)：只能向右上擴展
        預期：1
        """
        grid = ["aaa", "aaa", "aaa"]
        result = self.find_largest_square(grid, 2, 0)
        self.assertEqual(result, 1)
    
    def test_corner_bottom_right(self):
        """
        測試右下角查詢
        網格（3x3）：
        aaa
        aaa
        aaa
        查詢 (2, 2)：只能向左上擴展
        預期：1
        """
        grid = ["aaa", "aaa", "aaa"]
        result = self.find_largest_square(grid, 2, 2)
        self.assertEqual(result, 1)
    
    # ===== 特殊情況測試 =====
    
    def test_5x5_grid_all_same(self):
        """
        測試 5x5 網格，所有字元相同
        網格：
        aaaaa
        aaaaa
        aaaaa
        aaaaa
        aaaaa
        查詢中心 (2, 2)
        預期：5（整個網格都是同一個字元）
        """
        grid = [
            "aaaaa",
            "aaaaa",
            "aaaaa",
            "aaaaa",
            "aaaaa"
        ]
        result = self.find_largest_square(grid, 2, 2)
        self.assertEqual(result, 5)
    
    def test_7x7_cross_pattern(self):
        """
        測試十字形圖案
        網格（7x7）：
        aaabbaa
        aaabbaa
        aaabbaa
        bbbbbbb
        aaabbaa
        aaabbaa
        aaabbaa
        
        查詢中心 (3, 3) 的 'b'
        預期：1（中心 'b' 周圍有 'a'，只能是 1）
        注：正方形邊長 3 時，範圍 [2,4]x[2,4] 會包含 'a'
        """
        grid = [
            "aaabbaa",
            "aaabbaa",
            "aaabbaa",
            "bbbbbbb",
            "aaabbaa",
            "aaabbaa",
            "aaabbaa"
        ]
        result = self.find_largest_square(grid, 3, 3)
        self.assertEqual(result, 1)
    
    def test_mixed_characters(self):
        """
        測試多種字元
        網格：
        abcde
        bcdef
        cdefg
        defgh
        efghi
        
        查詢 (2, 2) 的 'f'
        預期：1（每個位置的字元都不同）
        """
        grid = [
            "abcde",
            "bcdef",
            "cdefg",
            "defgh",
            "efghi"
        ]
        result = self.find_largest_square(grid, 2, 2)
        self.assertEqual(result, 1)
    
    # ===== 線性網格測試 =====
    
    def test_horizontal_line(self):
        """
        測試水平線
        網格（1x5）：
        aaaaa
        
        查詢 (0, 2)
        預期：1（不能垂直擴展）
        """
        grid = ["aaaaa"]
        result = self.find_largest_square(grid, 0, 2)
        self.assertEqual(result, 1)
    
    def test_vertical_line(self):
        """
        測試垂直線
        網格（5x1）：
        a
        a
        a
        a
        a
        
        查詢 (2, 0)
        預期：1（不能水平擴展）
        """
        grid = ["a", "a", "a", "a", "a"]
        result = self.find_largest_square(grid, 2, 0)
        self.assertEqual(result, 1)


class TestQ10908EdgeCases(unittest.TestCase):
    """
    額外的邊界情況測試
    """
    
    def find_largest_square(self, grid, r, c):
        """解題函數（同上）"""
        m = len(grid)
        n = len(grid[0]) if m > 0 else 0
        center_char = grid[r][c]
        max_length = 1
        max_distance = min(r, c, m - 1 - r, n - 1 - c)
        max_possible = 2 * max_distance + 1
        
        for length in range(1, max_possible + 1, 2):
            distance = length // 2
            valid = True
            
            for i in range(r - distance, r + distance + 1):
                for j in range(c - distance, c + distance + 1):
                    if i < 0 or i >= m or j < 0 or j >= n:
                        valid = False
                        break
                    if grid[i][j] != center_char:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                max_length = length
            else:
                break
        
        return max_length
    
    def test_large_grid_100x100(self):
        """
        測試最大尺寸網格（100x100）
        預期：應該在合理時間內完成
        """
        # 創建 100x100 的網格，全是 'a'
        grid = ['a' * 100 for _ in range(100)]
        result = self.find_largest_square(grid, 50, 50)
        # 中心點 (50, 50) 距離最近邊界 50 格
        # 所以最大邊長應為 2*50 + 1 = 101
        # 但邊界只有 100，所以應該是 100
        self.assertEqual(result, 99)
    
    def test_checkerboard_pattern(self):
        """
        測試棋盤圖案
        網格：
        aba
        bab
        aba
        
        查詢 (1, 1) 的 'a'
        預期：1（周圍都是 'b'）
        """
        grid = ["aba", "bab", "aba"]
        result = self.find_largest_square(grid, 1, 1)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    # 執行所有測試
    unittest.main(verbosity=2)
