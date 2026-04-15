"""
反正切計算 π (Arctan Pi) - 單元測試

題目說明：
- 使用 arctan(1/a) = arctan(1/b) + arctan(1/c) 公式
- 其中 a, b, c 為正整數
- 求給定 a 時，b + c 的最小值

單元測試：測試各種 a 值的分解
"""

import unittest
import math


def find_arctan_decomposition(a):
    """
    找出 arctan(1/a) = arctan(1/b) + arctan(1/c) 中 b + c 的最小值

    使用公式：arctan(p) + arctan(q) = arctan((p+q)/(1-pq))

    令 p = 1/b, q = 1/c，則：
    arctan(1/b) + arctan(1/c) = arctan((1/b + 1/c) / (1 - 1/(bc)))
                               = arctan((b+c) / (bc-1))

    要使其等於 arctan(1/a)，需要：
    (b+c) / (bc-1) = 1/a
    即：a(b+c) = bc-1
        ab + ac = bc - 1
        bc - ab - ac = 1
        b(c-a) - ac = 1
        b(c-a) = ac + 1
        b = (ac + 1) / (c - a)

    參數：
        a: 正整數

    返回值：
        (b, c, b+c) 使得 b + c 最小
    """
    min_sum = float("inf")
    best_b, best_c = None, None

    # 特殊情況：a = 1
    # arctan(1) = arctan(1/2) + arctan(1/3)
    if a == 1:
        return 2, 3, 5

    # 搜索所有可能的 c 值
    # c 必須大於 a（確保分母 c-a > 0）
    # 搜索範圍設定到合理上限
    for c in range(a + 1, a * a + 1):
        # 檢查 (ac + 1) 是否能被 (c - a) 整除
        numerator = a * c + 1
        denominator = c - a

        if numerator % denominator == 0:
            b = numerator // denominator

            # b 必須是正整數
            if b > 0:
                current_sum = b + c
                if current_sum < min_sum:
                    min_sum = current_sum
                    best_b = b
                    best_c = c

    return best_b, best_c, min_sum


def find_arctan_decomposition_verify(a, b, c):
    """
    驗證 arctan(1/a) 是否等於 arctan(1/b) + arctan(1/c)

    參數：
        a, b, c: 正整數

    返回值：
        True 如果相等，False 否則
    """
    # 計算左邊
    left = math.atan(1.0 / a)

    # 計算右邊
    right = math.atan(1.0 / b) + math.atan(1.0 / c)

    # 比較（允許浮點誤差）
    return abs(left - right) < 1e-9


class TestArctanPi(unittest.TestCase):
    """反正切計算 π 單元測試類別"""

    def test_a_equals_2(self):
        """測試 1: a = 2"""
        # arctan(1/2) = arctan(1/3) + arctan(1/5)
        # 驗證：(1/3 + 1/5) / (1 - 1/15) = (8/15) / (14/15) = 8/14 = 4/7 ≠ 1/2
        # 正確應該是：b(c-2) = 2c+1，即 b = (2c+1)/(c-2)
        # c=3: b = 7/1 = 7, sum = 10
        # c=4: b = 9/2 = 不是整數
        # c=5: b = 11/3 = 不是整數
        # ...
        # 搜索找出最小值

        b, c, min_sum = find_arctan_decomposition(2)

        # 驗證結果
        self.assertIsNotNone(b)
        self.assertIsNotNone(c)
        self.assertTrue(find_arctan_decomposition_verify(2, b, c))

        print(f"a=2: b={b}, c={c}, sum={min_sum}")

    def test_a_equals_3(self):
        """測試 2: a = 3"""
        b, c, min_sum = find_arctan_decomposition(3)

        self.assertIsNotNone(b)
        self.assertIsNotNone(c)
        self.assertTrue(find_arctan_decomposition_verify(3, b, c))

        print(f"a=3: b={b}, c={c}, sum={min_sum}")

    def test_a_equals_4(self):
        """測試 3: a = 4"""
        # arctan(1/4) = arctan(1/b) + arctan(1/c)
        # b = (4c + 1) / (c - 4)
        # c=5: b = 21/1 = 21, sum = 26
        # c=6: b = 25/2 = 不是整數
        # c=7: b = 29/3 = 不是整數
        # ...

        b, c, min_sum = find_arctan_decomposition(4)

        self.assertIsNotNone(b)
        self.assertIsNotNone(c)
        self.assertTrue(find_arctan_decomposition_verify(4, b, c))

        print(f"a=4: b={b}, c={c}, sum={min_sum}")

    def test_a_equals_5(self):
        """測試 4: a = 5"""
        b, c, min_sum = find_arctan_decomposition(5)

        self.assertIsNotNone(b)
        self.assertIsNotNone(c)
        self.assertTrue(find_arctan_decomposition_verify(5, b, c))

        print(f"a=5: b={b}, c={c}, sum={min_sum}")

    def test_a_equals_1(self):
        """測試 5: a = 1 (特殊情況)"""
        # arctan(1/1) = arctan(1/b) + arctan(1/c)
        # b = (c + 1) / (c - 1)
        # c=2: b = 3/1 = 3, sum = 5
        # 驗證：arctan(1) = arctan(1/3) + arctan(1/2)

        b, c, min_sum = find_arctan_decomposition(1)

        self.assertIsNotNone(b)
        self.assertIsNotNone(c)
        self.assertTrue(find_arctan_decomposition_verify(1, b, c))

        print(f"a=1: b={b}, c={c}, sum={min_sum}")

    def test_verify_formula(self):
        """測試 6: 驗證 arctan 相加公式"""
        # 已知：arctan(1/2) + arctan(1/3) = arctan(1)
        left = math.atan(1.0 / 1)
        right = math.atan(1.0 / 2) + math.atan(1.0 / 3)

        self.assertAlmostEqual(left, right, places=9)

    def test_a_equals_10(self):
        """測試 7: a = 10"""
        b, c, min_sum = find_arctan_decomposition(10)

        self.assertIsNotNone(b)
        self.assertIsNotNone(c)
        self.assertTrue(find_arctan_decomposition_verify(10, b, c))

        print(f"a=10: b={b}, c={c}, sum={min_sum}")

    def test_multiple_values(self):
        """測試 8: 多個 a 值"""
        for a in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            b, c, min_sum = find_arctan_decomposition(a)

            self.assertIsNotNone(b, f"Failed for a={a}")
            self.assertIsNotNone(c, f"Failed for a={a}")
            self.assertTrue(
                find_arctan_decomposition_verify(a, b, c),
                f"Verification failed for a={a}, b={b}, c={c}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
