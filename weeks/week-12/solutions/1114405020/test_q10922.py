"""
UVA 10922 - 2 the 9s 單元測試

9 的深度（9-degree）：
- 如果數字是 9 的倍數，計算其各位數字之和
- 重複此過程直到得到 9
- 計數重複的次數即為 9 的深度

測試涵蓋：
1. 基本的 9 的倍數判斷
2. 9 的深度計算
3. 邊界情況
4. 大數字處理
"""

import unittest
from solution_q10922 import calculate_9_degree, is_multiple_of_9, sum_digits


class TestUVA10922(unittest.TestCase):
    """UVA 10922 - 2 the 9s 測試用例"""

    # ========== 測試：9 的倍數判斷 ==========

    def test_single_digit_9_is_multiple(self):
        """測試：單個數字 9 是 9 的倍數"""
        self.assertTrue(is_multiple_of_9(9))

    def test_single_digit_not_multiple(self):
        """測試：單個數字 8 不是 9 的倍數"""
        self.assertFalse(is_multiple_of_9(8))

    def test_18_is_multiple_of_9(self):
        """測試：18 = 2*9 是 9 的倍數"""
        self.assertTrue(is_multiple_of_9(18))

    def test_27_is_multiple_of_9(self):
        """測試：27 = 3*9 是 9 的倍數"""
        self.assertTrue(is_multiple_of_9(27))

    def test_10_is_not_multiple(self):
        """測試：10 不是 9 的倍數"""
        self.assertFalse(is_multiple_of_9(10))

    def test_99_is_multiple_of_9(self):
        """測試：99 = 11*9 是 9 的倍數"""
        self.assertTrue(is_multiple_of_9(99))

    def test_100_is_not_multiple(self):
        """測試：100 不是 9 的倍數"""
        self.assertFalse(is_multiple_of_9(100))

    # ========== 測試：各位數字之和 ==========

    def test_sum_digits_9(self):
        """測試：9 的各位數字之和為 9"""
        self.assertEqual(sum_digits(9), 9)

    def test_sum_digits_18(self):
        """測試：18 的各位數字之和為 1+8=9"""
        self.assertEqual(sum_digits(18), 9)

    def test_sum_digits_123(self):
        """測試：123 的各位數字之和為 1+2+3=6"""
        self.assertEqual(sum_digits(123), 6)

    def test_sum_digits_999(self):
        """測試：999 的各位數字之和為 9+9+9=27"""
        self.assertEqual(sum_digits(999), 27)

    # ========== 測試：9 的深度計算 ==========

    def test_degree_of_9(self):
        """測試：9 的深度為 1（9 已經是 9）"""
        self.assertEqual(calculate_9_degree(9), 1)

    def test_degree_of_18(self):
        """測試：18 的深度為 1
        
        計算過程：
        - 18: 1+8=9
        - 9: 已經是 9，停止
        - 深度 = 1
        """
        self.assertEqual(calculate_9_degree(18), 1)

    def test_degree_of_27(self):
        """測試：27 的深度為 1
        
        計算過程：
        - 27: 2+7=9
        - 9: 已經是 9，停止
        - 深度 = 1
        """
        self.assertEqual(calculate_9_degree(27), 1)

    def test_degree_of_99(self):
        """測試：99 的深度為 1
        
        計算過程：
        - 99: 9+9=18
        - 18: 1+8=9
        - 9: 已經是 9，停止
        - 深度 = 2
        """
        self.assertEqual(calculate_9_degree(99), 2)

    def test_degree_of_999(self):
        """測試：999 的深度
        
        計算過程：
        - 999: 9+9+9=27
        - 27: 2+7=9
        - 9: 已經是 9，停止
        - 深度 = 2
        """
        self.assertEqual(calculate_9_degree(999), 2)

    def test_degree_of_9999(self):
        """測試：9999 的深度
        
        計算過程：
        - 9999: 9+9+9+9=36
        - 36: 3+6=9
        - 9: 已經是 9，停止
        - 深度 = 2
        """
        self.assertEqual(calculate_9_degree(9999), 2)

    def test_degree_of_99999(self):
        """測試：99999 的深度
        
        計算過程：
        - 99999: 9+9+9+9+9=45
        - 45: 4+5=9
        - 9: 已經是 9，停止
        - 深度 = 2
        """
        self.assertEqual(calculate_9_degree(99999), 2)

    def test_degree_of_999999999(self):
        """測試：999999999 的深度（九個 9）
        
        計算過程：
        - 999999999: 9*9=81
        - 81: 8+1=9
        - 9: 已經是 9，停止
        - 深度 = 2
        """
        self.assertEqual(calculate_9_degree(999999999), 2)

    # ========== 測試：邊界情況 ==========

    def test_large_number_is_multiple(self):
        """測試：大數字 1000000008 是 9 的倍數
        
        計算：1+0+0+0+0+0+0+0+0+8=9，是 9 的倍數
        """
        self.assertTrue(is_multiple_of_9(1000000008))

    def test_large_number_degree(self):
        """測試：大數字的 9 的深度
        
        1000000008: 1+0+0+0+0+0+0+0+0+8=9
        深度 = 1
        """
        self.assertEqual(calculate_9_degree(1000000008), 1)

    def test_very_large_number(self):
        """測試：非常大的數字（20 位數）
        
        99999999999999999999 是 9 的倍數
        其深度計算
        """
        large_num = 99999999999999999999
        self.assertTrue(is_multiple_of_9(large_num))
        # 各位數字之和 = 9*20 = 180
        # 180: 1+8+0=9
        # 深度 = 2
        self.assertEqual(calculate_9_degree(large_num), 2)

    def test_not_multiple_of_9_output_check(self):
        """測試：非 9 的倍數數字應該輸出特定格式"""
        # 這個測試用於驗證非倍數的情況
        self.assertFalse(is_multiple_of_9(10))
        self.assertFalse(is_multiple_of_9(100))
        self.assertFalse(is_multiple_of_9(12345))  # 1+2+3+4+5=15，不是 9 的倍數


class TestIntegration(unittest.TestCase):
    """整合測試 - 測試完整的程式流程"""

    def test_integration_multiple_inputs(self):
        """測試：多個輸入的綜合處理"""
        test_cases = [
            (9, True, 1),
            (18, True, 1),
            (27, True, 1),
            (99, True, 2),
            (10, False, None),
            (100, False, None),
            (999, True, 2),
        ]
        
        for num, is_mult, degree in test_cases:
            with self.subTest(num=num):
                self.assertEqual(is_multiple_of_9(num), is_mult)
                if is_mult:
                    self.assertEqual(calculate_9_degree(num), degree)


if __name__ == '__main__':
    unittest.main()
