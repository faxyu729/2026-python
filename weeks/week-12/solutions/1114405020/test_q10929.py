"""
UVA 10929 - Let's Play Euclid
單元測試（15+ 個測試用例）

測試包括：
- 官方範例
- 邊界情況
- 大數字
- 特殊情況
"""

import unittest
import sys
from io import StringIO
from pathlib import Path

# 導入解決方案
sys.path.insert(0, str(Path(__file__).parent))
from solution_q10929 import is_multiple_of_11


class TestQ10929(unittest.TestCase):
    """UVA 10929 的單元測試類"""
    
    # ==================== 基本測試 ====================
    
    def test_single_digit_zero(self):
        """測試單位數：0（零是 11 的倍數）"""
        self.assertTrue(is_multiple_of_11("0"))
    
    def test_single_digit_11_multiples(self):
        """測試單位數中 11 的倍數"""
        # 0 是所有非零整數的倍數
        self.assertTrue(is_multiple_of_11("0"))
    
    def test_single_digit_non_multiples(self):
        """測試單位數中不是 11 的倍數的數字"""
        # 1-10 都不是 11 的倍數
        for i in range(1, 10):
            with self.subTest(i=i):
                self.assertFalse(is_multiple_of_11(str(i)))
    
    # ==================== 兩位數測試 ====================
    
    def test_two_digit_11(self):
        """測試兩位數：11 是 11 的倍數"""
        # 11 的第 1 位是 1（奇數位），第 2 位是 1（偶數位）
        # 奇數位和：1，偶數位和：1，差值：0
        self.assertTrue(is_multiple_of_11("11"))
    
    def test_two_digit_22(self):
        """測試兩位數：22 是 11 的倍數"""
        # 22 的第 1 位是 2（奇數位），第 2 位是 2（偶數位）
        # 奇數位和：2，偶數位和：2，差值：0
        self.assertTrue(is_multiple_of_11("22"))
    
    def test_two_digit_33(self):
        """測試兩位數：33 是 11 的倍數"""
        self.assertTrue(is_multiple_of_11("33"))
    
    def test_two_digit_99(self):
        """測試兩位數：99 是 11 的倍數"""
        self.assertTrue(is_multiple_of_11("99"))
    
    def test_two_digit_12(self):
        """測試兩位數：12 不是 11 的倍數"""
        # 12 的第 1 位是 2（奇數位），第 2 位是 1（偶數位）
        # 奇數位和：2，偶數位和：1，差值：1
        self.assertFalse(is_multiple_of_11("12"))
    
    def test_two_digit_10(self):
        """測試兩位數：10 不是 11 的倍數"""
        self.assertFalse(is_multiple_of_11("10"))
    
    # ==================== 三位數測試 ====================
    
    def test_three_digit_121(self):
        """測試三位數：121 是 11 的倍數（121 = 11 × 11）"""
        # 121: 位置 1(奇) 2(偶) 3(奇)，數字 1 2 1
        # 奇數位和：1 + 1 = 2，偶數位和：2
        # 差值：2 - 2 = 0
        self.assertTrue(is_multiple_of_11("121"))
    
    def test_three_digit_123(self):
        """測試三位數：123 不是 11 的倍數"""
        # 123: 位置 1(奇) 2(偶) 3(奇)，數字 3 2 1
        # 奇數位和：3 + 1 = 4，偶數位和：2
        # 差值：4 - 2 = 2
        self.assertFalse(is_multiple_of_11("123"))
    
    def test_three_digit_110(self):
        """測試三位數：110 是 11 的倍數"""
        # 110: 位置 1(奇) 2(偶) 3(奇)，數字 0 1 1
        # 奇數位和：0 + 1 = 1，偶數位和：1
        # 差值：1 - 1 = 0
        self.assertTrue(is_multiple_of_11("110"))
    
    def test_three_digit_143(self):
        """測試三位數：143 是 11 的倍數（143 = 11 × 13）"""
        # 143: 位置 1(奇) 2(偶) 3(奇)，數字 3 4 1
        # 奇數位和：3 + 1 = 4，偶數位和：4
        # 差值：4 - 4 = 0
        self.assertTrue(is_multiple_of_11("143"))
    
    # ==================== 四位數及以上 ====================
    
    def test_four_digit_1111(self):
        """測試四位數：1111 是 11 的倍數（1111 = 11 × 101）"""
        # 1111: 位置 1(奇) 2(偶) 3(奇) 4(偶)，數字 1 1 1 1
        # 奇數位和：1 + 1 = 2，偶數位和：1 + 1 = 2
        # 差值：2 - 2 = 0
        self.assertTrue(is_multiple_of_11("1111"))
    
    def test_four_digit_1234(self):
        """測試四位數：1234 不是 11 的倍數"""
        # 1234: 位置 1(奇) 2(偶) 3(奇) 4(偶)，數字 4 3 2 1
        # 奇數位和：4 + 2 = 6，偶數位和：3 + 1 = 4
        # 差值：6 - 4 = 2
        self.assertFalse(is_multiple_of_11("1234"))
    
    def test_five_digit_10989(self):
        """測試五位數：10989 是 11 的倍數（10989 = 11 × 999）"""
        # 10989: 位置 1(奇) 2(偶) 3(奇) 4(偶) 5(奇)
        #        數字 9    8     9    0     1
        # 奇數位和：9 + 9 + 1 = 19，偶數位和：8 + 0 = 8
        # 差值：19 - 8 = 11，11 % 11 = 0
        self.assertTrue(is_multiple_of_11("10989"))
    
    # ==================== 邊界情況 ====================
    
    def test_leading_zero(self):
        """測試帶前導零的數字：01 應理解為 1"""
        # 01: 位置 1(奇) 2(偶)，數字 1 0
        # 奇數位和：1，偶數位和：0
        # 差值：1
        self.assertFalse(is_multiple_of_11("01"))
    
    def test_all_zeros(self):
        """測試全零數字：00...0"""
        # 000: 位置都是 0
        # 奇數位和：0，偶數位和：0
        # 差值：0
        self.assertTrue(is_multiple_of_11("000"))
    
    # ==================== 大數字測試 ====================
    
    def test_large_number_1(self):
        """測試大數字：1000000000（十億）"""
        # 1000000000: 位置 1-10，只有位置 10 是 1（偶數位），其他都是 0
        # 奇數位和：0，偶數位和：1
        # 差值：-1，-1 % 11 = 10
        self.assertFalse(is_multiple_of_11("1000000000"))
    
    def test_large_number_2(self):
        """測試大數字：999999999999（十二個 9）"""
        # 十二個 9
        # 奇數位和（第 1、3、5、7、9、11 位）：6 × 9 = 54
        # 偶數位和（第 2、4、6、8、10、12 位）：6 × 9 = 54
        # 差值：54 - 54 = 0
        self.assertTrue(is_multiple_of_11("999999999999"))
    
    def test_large_number_3(self):
        """測試大數字：1234567890123"""
        # 檢查這是否是 11 的倍數
        # 位置 1(奇) 2(偶) 3(奇) 4(偶) 5(奇) 6(偶) 7(奇) 8(偶) 9(奇) 10(偶) 11(奇) 12(偶) 13(奇)
        # 數字 3    2    1    0    9    8    7    6    5    4    3    2    1
        # 奇數位和：3 + 1 + 9 + 7 + 5 + 3 + 1 = 29
        # 偶數位和：2 + 0 + 8 + 6 + 4 + 2 = 22
        # 差值：29 - 22 = 7
        self.assertFalse(is_multiple_of_11("1234567890123"))
    
    # ==================== 官方範例測試 ====================
    
    def test_example_1(self):
        """測試官方範例：100 是 11 的倍數嗎？"""
        # 100: 位置 1(奇) 2(偶) 3(奇)，數字 0 0 1
        # 奇數位和：0 + 1 = 1，偶數位和：0
        # 差值：1，不是 11 的倍數
        self.assertFalse(is_multiple_of_11("100"))
    
    def test_example_2(self):
        """測試官方範例：121 是 11 的倍數嗎？"""
        self.assertTrue(is_multiple_of_11("121"))
    
    # ==================== 特殊模式測試 ====================
    
    def test_alternating_pattern_11111(self):
        """測試重複模式：11111（五個 1）"""
        # 11111: 位置 1(奇) 2(偶) 3(奇) 4(偶) 5(奇)
        # 奇數位和：1 + 1 + 1 = 3，偶數位和：1 + 1 = 2
        # 差值：3 - 2 = 1
        self.assertFalse(is_multiple_of_11("11111"))
    
    def test_palindrome_1221(self):
        """測試回文數字：1221"""
        # 1221: 位置 1(奇) 2(偶) 3(奇) 4(偶)，數字 1 2 2 1
        # 奇數位和：1 + 2 = 3，偶數位和：2 + 1 = 3
        # 差值：3 - 3 = 0
        self.assertTrue(is_multiple_of_11("1221"))
    
    def test_negative_difference(self):
        """測試負差值的情況：10"""
        # 10: 位置 1(奇) 2(偶)，數字 0 1
        # 奇數位和：0，偶數位和：1
        # 差值：-1，-1 % 11 = 10
        self.assertFalse(is_multiple_of_11("10"))
    
    def test_very_large_number(self):
        """測試非常大的數字：1000 位的數"""
        # 構造：10000...0001（1 後跟 998 個 0，再跟 1）
        large_num = "1" + "0" * 998 + "1"
        # 1000 位數字，位置 1(奇) 和位置 1000(偶)
        # 奇數位和：1（位置 1）
        # 偶數位和：1（位置 1000）
        # 差值：1 - 1 = 0，0 % 11 == 0，所以是 11 的倍數
        self.assertTrue(is_multiple_of_11(large_num))


class TestQ10929EdgeCases(unittest.TestCase):
    """邊界情況和極端情況測試"""
    
    def test_string_type_handling(self):
        """測試字符串類型輸入"""
        # 函數應該能正確處理字符串
        result = is_multiple_of_11("121")
        self.assertTrue(isinstance(result, bool))
    
    def test_multiple_of_11_up_to_200(self):
        """測試 11 的所有倍數直到 200"""
        # 11 的倍數：11, 22, 33, ..., 198
        for i in range(1, 19):
            multiple = 11 * i
            with self.subTest(multiple=multiple):
                self.assertTrue(is_multiple_of_11(str(multiple)))
    
    def test_non_multiples_near_multiples(self):
        """測試 11 倍數附近的非倍數"""
        test_cases = [
            ("10", False),  # 11 - 1
            ("12", False),  # 11 + 1
            ("21", False),  # 22 - 1
            ("23", False),  # 22 + 1
        ]
        for num_str, expected in test_cases:
            with self.subTest(num=num_str):
                self.assertEqual(is_multiple_of_11(num_str), expected)


def run_tests():
    """運行所有測試"""
    # 創建測試套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加測試類
    suite.addTests(loader.loadTestsFromTestCase(TestQ10929))
    suite.addTests(loader.loadTestsFromTestCase(TestQ10929EdgeCases))
    
    # 運行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回是否所有測試都通過
    return result.wasSuccessful()


if __name__ == "__main__":
    # 運行測試
    success = run_tests()
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("測試完成！")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
