"""
UVA 10931 測試用例 - 奇偶性校驗位
用來測試二進位轉換和 1 的個數計算的單元測試
"""

import unittest
from io import StringIO
import sys


def count_ones_in_binary(n):
    """
    計算整數的二進位表示中 1 的個數
    
    Args:
        n: 正整數 (1 <= n <= 2,147,483,647)
    
    Returns:
        二進位中 1 的個數
    """
    # 轉換為二進位字符串，移除 '0b' 前綴，計算 '1' 的個數
    return bin(n).count('1')


class TestUVA10931(unittest.TestCase):
    """
    UVA 10931 - 奇偶性校驗位測試類別
    """
    
    # ===== 基本測試用例 =====
    
    def test_single_bit_one(self):
        """測試：只有一個 1 位元的數字 (1 的個數為奇數)"""
        # 1 的二進位為 1，只有 1 個 1
        self.assertEqual(count_ones_in_binary(1), 1)
        self.assertEqual(count_ones_in_binary(1) % 2, 1)
    
    def test_single_bit_two(self):
        """測試：2 的二進位為 10，只有 1 個 1"""
        # 2 的二進位為 10，只有 1 個 1
        self.assertEqual(count_ones_in_binary(2), 1)
        self.assertEqual(count_ones_in_binary(2) % 2, 1)
    
    def test_single_bit_four(self):
        """測試：4 的二進位為 100，只有 1 個 1"""
        # 4 的二進位為 100
        self.assertEqual(count_ones_in_binary(4), 1)
        self.assertEqual(count_ones_in_binary(4) % 2, 1)
    
    def test_three(self):
        """測試：3 的二進位為 11，有 2 個 1"""
        # 3 的二進位為 11，有 2 個 1
        self.assertEqual(count_ones_in_binary(3), 2)
        self.assertEqual(count_ones_in_binary(3) % 2, 0)
    
    def test_seven(self):
        """測試：7 的二進位為 111，有 3 個 1"""
        # 7 的二進位為 111，有 3 個 1
        self.assertEqual(count_ones_in_binary(7), 3)
        self.assertEqual(count_ones_in_binary(7) % 2, 1)
    
    def test_fifteen(self):
        """測試：15 的二進位為 1111，有 4 個 1"""
        # 15 的二進位為 1111，有 4 個 1
        self.assertEqual(count_ones_in_binary(15), 4)
        self.assertEqual(count_ones_in_binary(15) % 2, 0)
    
    # ===== 邊界測試 =====
    
    def test_minimum_value(self):
        """測試：最小值 1"""
        # 1 是最小的輸入值，二進位為 1
        result = count_ones_in_binary(1)
        self.assertGreater(result, 0)
        self.assertEqual(result, 1)
    
    def test_maximum_value(self):
        """測試：最大值 2,147,483,647 (2^31 - 1，全是 1)"""
        # 2^31 - 1 的二進位全是 1，共 31 個 1
        max_val = 2147483647
        ones_count = count_ones_in_binary(max_val)
        self.assertEqual(ones_count, 31)
        self.assertEqual(ones_count % 2, 1)
    
    def test_power_of_two(self):
        """測試：2 的冪次 (只有 1 個 1)"""
        # 2 的冪次數字二進位中只有 1 個 1
        powers_of_two = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
        for power in powers_of_two:
            with self.subTest(power=power):
                self.assertEqual(count_ones_in_binary(power), 1)
    
    def test_all_ones(self):
        """測試：全是 1 的二進位 (例如 1, 3, 7, 15, 31, 63, 127)"""
        # 這些數字的二進位表示全是 1
        all_ones_numbers = [1, 3, 7, 15, 31, 63, 127, 255, 511, 1023]
        expected_ones = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for num, expected in zip(all_ones_numbers, expected_ones):
            with self.subTest(num=num):
                self.assertEqual(count_ones_in_binary(num), expected)
    
    # ===== 中等大小數字測試 =====
    
    def test_common_numbers(self):
        """測試：常見的中等大小數字"""
        test_cases = [
            (10, 2),      # 10 = 1010 (2個1)
            (100, 3),     # 100 = 1100100 (3個1)
            (1000, 6),    # 1000 = 1111101000 (6個1)
            (999, 8),     # 999 = 1111100111 (8個1)
            (12345, 6),   # 12345 = 11000000111001 (6個1)
        ]
        for num, expected_ones in test_cases:
            with self.subTest(num=num):
                self.assertEqual(count_ones_in_binary(num), expected_ones)
    
    # ===== 奇偶性測試 =====
    
    def test_parity_odd(self):
        """測試：奇偶性為奇數的情況"""
        # 1 的個數為奇數的數字
        odd_parity_numbers = [1, 2, 4, 7, 8, 11, 13, 14]
        for num in odd_parity_numbers:
            with self.subTest(num=num):
                ones_count = count_ones_in_binary(num)
                self.assertEqual(ones_count % 2, 1, f"{num} 的奇偶性應該是奇數")
    
    def test_parity_even(self):
        """測試：奇偶性為偶數的情況"""
        # 1 的個數為偶數的數字
        even_parity_numbers = [3, 5, 6, 9, 10, 12, 15]
        for num in even_parity_numbers:
            with self.subTest(num=num):
                ones_count = count_ones_in_binary(num)
                self.assertEqual(ones_count % 2, 0, f"{num} 的奇偶性應該是偶數")
    
    # ===== 特殊情況 =====
    
    def test_binary_conversion(self):
        """測試：確認二進位轉換正確"""
        test_cases = [
            (1, '1'),           # 1 的二進位為 1
            (2, '10'),          # 2 的二進位為 10
            (3, '11'),          # 3 的二進位為 11
            (5, '101'),         # 5 的二進位為 101
            (8, '1000'),        # 8 的二進位為 1000
            (255, '11111111'),  # 255 的二進位為 11111111
        ]
        for num, expected_binary in test_cases:
            with self.subTest(num=num):
                actual_binary = bin(num)[2:]  # 移除 '0b' 前綴
                self.assertEqual(actual_binary, expected_binary)
                self.assertEqual(actual_binary.count('1'), count_ones_in_binary(num))


class TestOutputFormat(unittest.TestCase):
    """
    測試輸出格式是否正確
    """
    
    def test_output_format(self):
        """測試：確認輸出格式是 'The parity of [B] is [P] (mod 2).'"""
        test_cases = [
            (1, "The parity of 1 is 1 (mod 2)."),
            (3, "The parity of 11 is 0 (mod 2)."),
            (7, "The parity of 111 is 1 (mod 2)."),
        ]
        
        for num, expected_output in test_cases:
            with self.subTest(num=num):
                binary = bin(num)[2:]
                parity = count_ones_in_binary(num) % 2
                output = f"The parity of {binary} is {parity} (mod 2)."
                self.assertEqual(output, expected_output)


if __name__ == '__main__':
    # 運行所有測試
    unittest.main(verbosity=2)
