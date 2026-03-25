"""
UVA 10057 - 找尋最優密碼 (詳細版本)

【問題背景】
在公元2200年，科學家遺忘了電腦密碼。
在夢中看到多個無號整數，需要找到一個密碼(整數A)。
該密碼使得 |X1-A| + |X2-A| + ... + |Xn-A| 最小。

【問題分析】
這是一個經典的最小化絕對偏差問題。
數學上，使得絕對值之和最小的點始終是中位數。

【核心原理 - 為什麼是中位數？】

考慮簡單例子: X = [1, 2, 8]

如果A=1: |1-1| + |2-1| + |8-1| = 0 + 1 + 7 = 8
如果A=2: |1-2| + |2-2| + |8-2| = 1 + 0 + 6 = 7
如果A=3: |1-3| + |2-3| + |8-3| = 2 + 1 + 5 = 8
如果A=4: |1-4| + |2-4| + |8-4| = 3 + 2 + 4 = 9
如果A=5: |1-5| + |2-5| + |8-5| = 4 + 3 + 3 = 10

最小值在A=2處達到(中位數)。

【數學證明概要】

設X1 ≤ X2 ≤ ... ≤ Xn (已排序)，中位數 M = X[(n+1)/2]

對於任何點A，其偏差之和可表示為:
  f(A) = Σ|Xi - A|

f(A)的導數(當存在時)為:
  f'(A) = Σ sign(A - Xi)

當A < X1: f'(A) = -n (負方向遞減)
當A > Xn: f'(A) = +n (正方向遞增)
當Xi ≤ A ≤ Xi+1: f'(A) = 2i - n

當n為奇數: 中位數處 f'(A) = 0，這是最小值點
當n為偶數: 任何介於 X[n/2] 和 X[n/2+1] 的點都有 f'(A) = 0

【演算法步驟】

1. 輸入n個數字
2. 排序這些數字
3. 找到中位數(或中位數範圍)
4. 計算有多少個數字等於選中的A
5. 計算有多少個整數可以達到最小值

【具體例子】

例1: 輸入 [1, 2, 3, 4, 5] (5個數字，奇數)
  排序後: [1, 2, 3, 4, 5]
  中位數: 3 (index = 2)
  等於3的計數: 1
  範圍計數: 1 (只有3能達到最小值)
  輸出: 3 1 1

例2: 輸入 [1, 2, 3, 4] (4個數字，偶數)
  排序後: [1, 2, 3, 4]
  下中位數: 2 (index = 1)
  上中位數: 3 (index = 2)
  選擇A: 3 (上中位數)
  等於3的計數: 1
  範圍計數: 3 - 2 + 1 = 2 (2和3都能達到最小值)
  輸出: 3 1 2

例3: 輸入 [1, 1, 1, 10, 10, 10] (6個數字，偶數，有重複)
  排序後: [1, 1, 1, 10, 10, 10]
  下中位數: 1 (index = 2)
  上中位數: 10 (index = 3)
  選擇A: 10 (上中位數)
  等於10的計數: 3
  範圍計數: 10 - 1 + 1 = 10
  輸出: 10 3 10

【時間和空間複雜度】

時間複雜度:
  - 排序: O(n log n)
  - 計算結果: O(n)
  - 總計: O(n log n)

空間複雜度:
  - 排序需要額外空間: O(n)

【邊界情況處理】

1. n = 1: 唯一的點就是最優點
2. 所有數字相同: 中位數就是該數字
3. 數字範圍很大: 正確處理整數計算
4. 重複值: 中位數可能有多個相同值

"""


def find_optimal_password(numbers):
    """
    找到最優密碼(最小化絕對偏差和的整數)

    參數:
        numbers (list of int): 無號整數列表

    返回值:
        tuple: (A值, 等於A的計數, 能達到最小值的整數範圍)

    詳細說明:
        1. A值: 使得 Σ|Xi-A| 最小的整數A
        2. 等於A的計數: 在輸入中有多少個數字等於A
        3. 範圍: 有多少個整數A可以達到最小的 Σ|Xi-A|
    """

    # ===== 步驟1: 檢查輸入 =====
    n = len(numbers)

    # 邊界情況: 空輸入
    if n == 0:
        return 0, 0, 0

    # 邊界情況: 單一元素
    if n == 1:
        return numbers[0], 1, 1

    # ===== 步驟2: 排序以找到中位數 =====
    sorted_numbers = sorted(numbers)

    # ===== 步驟3: 區分奇偶情況 =====

    if n % 2 == 1:
        # 【奇數情況】
        # 中位數在 index = n // 2
        # 例: n=5時，index=2 (第3個元素，即中間的元素)

        median_index = n // 2
        a_value = sorted_numbers[median_index]

        # 奇數個元素時，只有一個點能達到最小值
        range_count = 1

    else:
        # 【偶數情況】
        # 兩個中位數在 index = n//2 - 1 和 n//2
        # 例: n=4時，index=1和2 (第2個和第3個元素)
        # 例: n=6時，index=2和3 (第3個和第4個元素)

        lower_median_index = n // 2 - 1
        upper_median_index = n // 2

        lower_median = sorted_numbers[lower_median_index]
        upper_median = sorted_numbers[upper_median_index]

        # 選擇上中位數作為答案
        # (根據UVA評測系統的期望)
        a_value = upper_median

        # 介於兩個中位數的所有整數都能達到最小值
        # 計算範圍內有多少個整數
        range_count = upper_median - lower_median + 1

    # ===== 步驟4: 計算等於A的數字個數 =====
    # 遍歷原輸入列表(不是排序後的)，計算有多少個等於A
    equal_count = 0
    for num in numbers:
        if num == a_value:
            equal_count += 1

    # ===== 步驟5: 返回結果 =====
    return a_value, equal_count, range_count


def validate_result(numbers, a, count, range_val):
    """
    驗證計算結果的正確性 (用於測試和調試)

    參數:
        numbers: 原始輸入
        a: 計算出的A值
        count: 等於A的計數
        range_val: 範圍計數

    返回值:
        bool: 結果是否有效
    """

    # 檢查: 等於A的計數是否正確
    actual_count = numbers.count(a)
    if actual_count != count:
        return False

    # 檢查: 計算最小值
    min_sum = sum(abs(num - a) for num in numbers)

    # 檢查: 所有在範圍內的點都能達到這個最小值
    n = len(numbers)
    if n % 2 == 1:
        # 奇數情況
        if range_val != 1:
            return False
    else:
        # 偶數情況
        sorted_nums = sorted(numbers)
        lower_median = sorted_nums[n // 2 - 1]
        upper_median = sorted_nums[n // 2]

        # 驗證範圍計數
        expected_range = upper_median - lower_median + 1
        if range_val != expected_range:
            return False

        # 驗證範圍內的所有點都能達到最小值
        for test_a in range(lower_median, upper_median + 1):
            test_sum = sum(abs(num - test_a) for num in numbers)
            if test_sum != min_sum:
                return False

    return True


def main():
    """
    主程式: 讀入測資並輸出結果

    輸入格式:
        第一行: n (數字個數，0表示結束)
        第二行: n個無號整數 (以空格分隔)

    輸出格式:
        三個整數: A值 等於A的計數 範圍計數

    例如:
        輸入:
        3
        1 2 3
        4
        1 2 3 4
        0

        輸出:
        2 1 1
        3 1 2
    """

    while True:
        # 讀入第一行
        try:
            n = int(input())
        except (EOFError, ValueError):
            break

        # 當n為0時，表示輸入結束
        if n == 0:
            break

        # 讀入n個數字
        try:
            numbers = list(map(int, input().split()))
        except (EOFError, ValueError):
            break

        # 檢查輸入數量是否正確
        if len(numbers) != n:
            continue

        # 解決問題
        a_value, equal_count, range_count = find_optimal_password(numbers)

        # 驗證結果 (可選，用於調試)
        # if not validate_result(numbers, a_value, equal_count, range_count):
        #     print("ERROR: Invalid result")
        #     continue

        # 輸出結果
        print(f"{a_value} {equal_count} {range_count}")


if __name__ == "__main__":
    main()
