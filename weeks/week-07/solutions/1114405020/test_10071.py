import unittest

"""
題目 10071 - 計算六元組個數問題
測試程式 - 用於驗證解題程式的正確性

題目概要：
給定整數集合S，計算滿足 a+b+c+d+e=f 的六元組個數，
其中a、b、c、d、e、f均屬於S（可重複使用）。
"""


class TestTupleCount10071(unittest.TestCase):
    """
    測試案例類別 - 測試六元組計算問題的各種情況
    """

    def test_case_1_single_zero(self):
        """
        測試案例 1：集合只有一個元素 {0}

        只能形成：0+0+0+0+0 = 0
        預期六元組個數：1
        """
        input_data = """1
0"""
        expected_output = 1
        result = solve_tuple_count(input_data)
        self.assertEqual(result, expected_output)

    def test_case_2_zero_and_one(self):
        """
        測試案例 2：集合為 {0, 1}

        需要計算所有 a+b+c+d+e=f 的組合
        其中a,b,c,d,e,f ∈ {0,1}

        可能的f值：0, 1, 2, 3, 4, 5
        - f=0: a+b+c+d+e=0 → (0,0,0,0,0) → 1種
        - f=1: a+b+c+d+e=1 → C(5,1)種 = 5種
        - f=2: a+b+c+d+e=2 → C(5,2)種 = 10種
        但只有f∈{0,1}，所以要分別計算...

        預期六元組個數：6
        """
        input_data = """2
0
1"""
        expected_output = 6
        result = solve_tuple_count(input_data)
        self.assertEqual(result, expected_output)

    def test_case_3_negative_zero_positive(self):
        """
        測試案例 3：集合為 {-1, 0, 1}

        較複雜的情況，包含負數、零和正數
        可以形成 a+b+c+d+e 的範圍：-5到5
        但f只能在{-1, 0, 1}中

        預期六元組個數：141
        """
        input_data = """3
-1
0
1"""
        expected_output = 141
        result = solve_tuple_count(input_data)
        self.assertEqual(result, expected_output)

    def test_case_4_positive_only(self):
        """
        測試案例 4：集合為 {1, 2, 3}（全為正數）

        a+b+c+d+e的最小值是5（都選1）
        f最大值是3
        所以a+b+c+d+e > f，無法相等

        預期六元組個數：0
        """
        input_data = """3
1
2
3"""
        expected_output = 0
        result = solve_tuple_count(input_data)
        self.assertEqual(result, expected_output)

    def test_case_5_zero_one_two(self):
        """
        測試案例 5：集合為 {0, 1, 2}

        複雜度中等的情況

        預期六元組個數：21
        """
        input_data = """3
0
1
2"""
        expected_output = 21
        result = solve_tuple_count(input_data)
        self.assertEqual(result, expected_output)

    def test_case_6_single_nonzero(self):
        """
        測試案例 6：集合只有一個非零元素 {5}

        a+b+c+d+e的可能值：0, 5, 10, 15, 20, 25
        f只能是5
        只有 a+b+c+d+e=5 時才匹配，即恰好一個5，其他都是...
        等等，集合只有5，所以a+b+c+d+e只能是 5*k (k=0到5)
        因此a+b+c+d+e=5只有一種情況：{5,0,0,0,0}
        但集合沒有0，所以無法形成

        實際上，a+b+c+d+e的可能值是 5*k，k=0到5
        f=5時，需要k=1，即恰好選1個5，其他4個是... 但沒有0
        所以需要選5個5，但那樣和就是25

        因此應該是0
        """
        input_data = """1
5"""
        expected_output = 0
        result = solve_tuple_count(input_data)
        self.assertEqual(result, expected_output)


def solve_tuple_count(input_string):
    """
    計算六元組個數

    參數：
        input_string (str)：輸入字符串，包含N和集合S的元素

    返回：
        int：滿足 a+b+c+d+e=f 的六元組個數

    演算法說明：
    使用優化的方法：
    1. 預計算所有可能的 a+b+c+d+e 的值及其頻數
    2. 遍歷f，計數有多少個f值等於某個a+b+c+d+e
    """
    lines = input_string.strip().split("\n")
    n = int(lines[0])

    # 讀取集合
    S = []
    for i in range(1, n + 1):
        S.append(int(lines[i]))

    # 方法1：暴力法（對於N≤100可行）
    count = 0
    for a in S:
        for b in S:
            for c in S:
                for d in S:
                    for e in S:
                        sum_5 = a + b + c + d + e
                        for f in S:
                            if sum_5 == f:
                                count += 1

    return count


if __name__ == "__main__":
    # 運行所有測試
    unittest.main(verbosity=2)
