import unittest
from io import StringIO
import sys

"""
題目 10062 - 乳牛排隊問題
測試程式 - 用於驗證解題程式的正確性

題目概要：
根據每頭乳牛前面編號較小的乳牛數量，重建正確的排列順序。
"""


class TestCow10062(unittest.TestCase):
    """
    測試案例類別 - 測試乳牛排隊問題的各種情況
    """

    def test_case_1_simple(self):
        """
        測試案例 1：簡單案例（遞增排列）
        N = 4
        位置2的牛：前面有1頭編號比它小的牛
        位置3的牛：前面有2頭編號比它小的牛
        位置4的牛：前面有3頭編號比它小的牛

        預期結果：[1, 2, 3, 4]
        驗證：
        - 位置1：牛1，前面0頭編號比它小
        - 位置2：牛2，前面1頭編號比它小(牛1) ✓
        - 位置3：牛3，前面2頭編號比它小(牛1,2) ✓
        - 位置4：牛4，前面3頭編號比它小(牛1,2,3) ✓
        """
        input_data = """4
1
2
3"""
        expected_output = [1, 2, 3, 4]
        result = solve_cow_problem(input_data)
        self.assertEqual(result, expected_output)

    def test_case_2_reverse_order(self):
        """
        測試案例 2：逆序排列
        N = 3
        位置2的牛：前面有1頭編號比它小
        位置3的牛：前面有2頭編號比它小

        測試輸入：
        3
        1
        2

        預期排列：[1, 2, 3]
        驗證：
        - 位置1：牛1，前面0頭編號<1
        - 位置2：牛2，前面1頭編號<2(牛1) ✓
        - 位置3：牛3，前面2頭編號<3(牛1,2) ✓
        """
        input_data = """3
1
2"""
        expected_output = [1, 2, 3]
        result = solve_cow_problem(input_data)
        self.assertEqual(result, expected_output)

    def test_case_3_mixed_order(self):
        """
        測試案例 3：混合排序
        N = 5
        測試複雜的混合編號排列
        輸入：[0, 0, 2, 1]
        預期排列：[5, 3, 1, 4, 2]
        """
        input_data = """5
0
0
2
1"""
        expected_output = [5, 3, 1, 4, 2]
        result = solve_cow_problem(input_data)
        self.assertEqual(result, expected_output)

    def test_case_4_minimum_case(self):
        """
        測試案例 4：最小案例
        N = 2
        只有兩頭牛
        """
        input_data = """2
0"""
        expected_output = [2, 1]
        result = solve_cow_problem(input_data)
        self.assertEqual(result, expected_output)

    def test_case_5_alternating(self):
        """
        測試案例 5：複雜交替排序
        N = 6
        測試複雜的交替排序情況
        輸入：[0, 1, 0, 2, 3]
        預期排列：[6, 2, 5, 1, 3, 4]
        """
        input_data = """6
0
1
0
2
3"""
        expected_output = [6, 2, 5, 1, 3, 4]
        result = solve_cow_problem(input_data)
        self.assertEqual(result, expected_output)


def solve_cow_problem(input_string):
    """
    解決乳牛排隊問題的主要函數

    參數：
        input_string (str)：輸入字符串，包含N和每個位置前面編號較小的牛數

    返回：
        list：重建後的乳牛排列順序

    演算法說明：
    使用回溯法逐位置確定乳牛編號：
    - 對於位置1，嘗試所有可能的編號
    - 對於位置i (i>=2)，嘗試編號使得前面編號<它的牛數 = info[i-2]
    - 如果某個選擇導致後續無法滿足約束，回溯並嘗試其他選擇
    - 最終返回滿足所有約束的排列
    """
    lines = input_string.strip().split("\n")
    n = int(lines[0])

    # 讀取每個位置前面編號較小的牛數量
    info = []
    for i in range(1, n):
        info.append(int(lines[i]))

    def can_place(pos, candidate, result):
        """檢查candidate是否可以放在pos位置"""
        if pos == 1:
            return True  # 位置1沒有約束

        # 計算result中有多少頭編號<candidate的牛
        target_smaller = info[pos - 2]
        smaller_count = sum(1 for x in result if x < candidate)
        return smaller_count == target_smaller

    def solve_recursive(pos, result, used):
        """
        遞歸求解：為位置pos選擇合適的編號

        參數：
            pos：當前要填充的位置（1到n）
            result：已填充位置的編號列表
            used：已使用編號的標記數組

        返回：
            找到的完整排列，或None如果無解
        """
        if pos == n + 1:
            # 已填充所有位置，找到解
            return result[:]

        # 嘗試每個未使用的編號
        for candidate in range(1, n + 1):
            if not used[candidate]:
                # 檢查該編號是否可以放在pos位置
                if can_place(pos, candidate, result):
                    # 標記為使用，並加入result
                    used[candidate] = True
                    result.append(candidate)

                    # 遞歸求解下一個位置
                    solution = solve_recursive(pos + 1, result, used)
                    if solution is not None:
                        return solution

                    # 如果無解，回溯
                    result.pop()
                    used[candidate] = False

        return None

    return solve_recursive(1, [], [False] * (n + 1))


if __name__ == "__main__":
    # 運行所有測試
    unittest.main(verbosity=2)
