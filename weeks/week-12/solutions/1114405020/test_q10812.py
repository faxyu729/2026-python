"""
UVA 10812 - Beat the Spread! 單元測試

題目說明：
根據兩隊得分的和 S 與差 D，求出兩隊各自的得分。
若無整數解或出現負數得分，則輸出 impossible。
"""

import unittest


class TestQ10812(unittest.TestCase):
    """
    針對 UVA 10812 問題的單元測試類別
    測試所有邊界情況和正常情況
    """
    
    def solve(self, s, d):
        """
        解題函數：根據和 s 與差 d 求兩隊得分
        
        數學原理：
        設兩隊得分為 a（較高分）和 b（較低分），其中 a >= b
        已知：
          - a + b = s（和）
          - a - b = d（差）
        
        聯立方程式求解：
          - a = (s + d) / 2
          - b = (s - d) / 2
        
        驗證條件：
          1. (s + d) 必須為偶數
          2. (s - d) 必須為偶數
          3. b >= 0（不能有負分）
        """
        # 檢查 (s + d) 是否為偶數
        if (s + d) % 2 != 0:
            return "impossible"
        
        # 檢查 (s - d) 是否為偶數
        if (s - d) % 2 != 0:
            return "impossible"
        
        # 計算較高分和較低分
        higher = (s + d) // 2
        lower = (s - d) // 2
        
        # 檢查較低分是否為非負
        if lower < 0:
            return "impossible"
        
        # 返回結果（較大的先）
        return f"{higher} {lower}"
    
    # ===== 基本測試用例 =====
    
    def test_normal_case_1(self):
        """
        測試正常情況 1
        輸入：S=40, D=20
        預期：30 10
        計算：a=(40+20)/2=30, b=(40-20)/2=10
        """
        result = self.solve(40, 20)
        self.assertEqual(result, "30 10")
    
    def test_normal_case_2(self):
        """
        測試正常情況 2
        輸入：S=100, D=50
        預期：75 25
        計算：a=(100+50)/2=75, b=(100-50)/2=25
        """
        result = self.solve(100, 50)
        self.assertEqual(result, "75 25")
    
    # ===== 邊界測試用例 =====
    
    def test_zero_scores(self):
        """
        測試零分情況
        輸入：S=0, D=0
        預期：0 0
        計算：a=(0+0)/2=0, b=(0-0)/2=0
        """
        result = self.solve(0, 0)
        self.assertEqual(result, "0 0")
    
    def test_large_difference(self):
        """
        測試差大於和的情況（無解）
        輸入：S=20, D=40
        預期：impossible（因為 b=(20-40)/2=-10 < 0）
        """
        result = self.solve(20, 40)
        self.assertEqual(result, "impossible")
    
    def test_negative_difference_not_allowed(self):
        """
        測試差超過總和導致負分
        輸入：S=50, D=60
        預期：impossible（b=(50-60)/2=-5 < 0）
        """
        result = self.solve(50, 60)
        self.assertEqual(result, "impossible")
    
    # ===== 奇偶性測試 =====
    
    def test_odd_sum_plus_diff(self):
        """
        測試 (S+D) 為奇數情況（無解）
        輸入：S=5, D=2（5+2=7，奇數）
        預期：impossible
        原因：(7)/2 不是整數
        """
        result = self.solve(5, 2)
        self.assertEqual(result, "impossible")
    
    def test_odd_sum_minus_diff(self):
        """
        測試 (S-D) 為奇數情況（無解）
        輸入：S=6, D=3（6-3=3，奇數）
        預期：impossible
        原因：(3)/2 不是整數
        """
        result = self.solve(6, 3)
        self.assertEqual(result, "impossible")
    
    # ===== 特殊情況測試 =====
    
    def test_both_scores_equal(self):
        """
        測試兩隊得分相等（差為 0）
        輸入：S=40, D=0
        預期：20 20
        計算：a=(40+0)/2=20, b=(40-0)/2=20
        """
        result = self.solve(40, 0)
        self.assertEqual(result, "20 20")
    
    def test_one_score_is_zero(self):
        """
        測試一隊得分為 0
        輸入：S=50, D=50
        預期：50 0
        計算：a=(50+50)/2=50, b=(50-50)/2=0
        """
        result = self.solve(50, 50)
        self.assertEqual(result, "50 0")
    
    def test_very_large_scores(self):
        """
        測試非常大的分數
        輸入：S=1000000, D=500000
        預期：750000 250000
        計算：a=(1000000+500000)/2=750000, b=(1000000-500000)/2=250000
        """
        result = self.solve(1000000, 500000)
        self.assertEqual(result, "750000 250000")
    
    def test_small_valid_case(self):
        """
        測試最小的有效情況
        輸入：S=2, D=0
        預期：1 1
        計算：a=(2+0)/2=1, b=(2-0)/2=1
        """
        result = self.solve(2, 0)
        self.assertEqual(result, "1 1")


class TestQ10812EdgeCases(unittest.TestCase):
    """
    針對 UVA 10812 的邊界情況測試
    """
    
    def solve(self, s, d):
        """解題函數（同上）"""
        if (s + d) % 2 != 0 or (s - d) % 2 != 0:
            return "impossible"
        
        higher = (s + d) // 2
        lower = (s - d) // 2
        
        if lower < 0:
            return "impossible"
        
        return f"{higher} {lower}"
    
    def test_maximum_difference_allowed(self):
        """
        測試差最大的有效情況（差等於和）
        輸入：S=100, D=100
        預期：100 0
        """
        result = self.solve(100, 100)
        self.assertEqual(result, "100 0")
    
    def test_just_beyond_max_difference(self):
        """
        測試超過最大差的情況
        輸入：S=100, D=101
        預期：impossible（b 會是負數）
        """
        result = self.solve(100, 101)
        self.assertEqual(result, "impossible")
    
    def test_odd_s_even_d(self):
        """
        測試 S 為奇數，D 為偶數
        輸入：S=5, D=2
        預期：impossible（S+D=7 為奇數）
        """
        result = self.solve(5, 2)
        self.assertEqual(result, "impossible")
    
    def test_even_s_odd_d(self):
        """
        測試 S 為偶數，D 為奇數
        輸入：S=6, D=3
        預期：impossible（S+D=9 為奇數）
        """
        result = self.solve(6, 3)
        self.assertEqual(result, "impossible")
    
    def test_both_odd(self):
        """
        測試 S 和 D 都是奇數
        輸入：S=7, D=3
        預期：impossible（S+D=10 為偶數，但 S-D=4 為偶數... 其實應該可以）
        等等，讓我重新計算：a=(7+3)/2=5, b=(7-3)/2=2
        所以應該返回 5 2
        """
        result = self.solve(7, 3)
        self.assertEqual(result, "5 2")


if __name__ == '__main__':
    # 執行所有測試
    # 使用 -v 選項以獲得詳細的測試輸出
    unittest.main(verbosity=2)
