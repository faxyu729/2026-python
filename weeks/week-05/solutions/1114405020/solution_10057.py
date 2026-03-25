"""
UVA 10057 - 找尋最優密碼

問題描述:
  給定n個無號整數，找到整數A使得絕對偏差之和最小
  |X1-A| + |X2-A| + ... + |Xn-A| 最小

輸出要求:
  1. A的值 (使最小值最小的整數)
  2. 等於A的數字個數 (計算有多少個Xi = A)
  3. 範圍計數 (有多少個整數可以達到最小值)

核心原理:
  - 最優點總是中位數
  - 奇數個元素: 中位數唯一
  - 偶數個元素: 介於兩個中位數的任何整數都是最優的
"""


def solve_password(numbers):
    """
    解決UVA 10057問題

    參數:
        numbers (list): 輸入的無號整數列表

    返回:
        tuple: (A值, 等於A的計數, 範圍計數)

    時間複雜度: O(n log n) - 主要用於排序
    空間複雜度: O(n) - 排序需要額外空間
    """
    n = len(numbers)

    # 對輸入進行排序以找到中位數
    sorted_nums = sorted(numbers)

    if n % 2 == 1:
        # 奇數個元素: 選擇中位數
        # 中位數是唯一的最優點
        a_value = sorted_nums[n // 2]
        range_count = 1  # 只有一個點達到最小值
    else:
        # 偶數個元素: 選擇上中位數
        # 介於下中位數和上中位數的任何整數都是最優的
        lower_median = sorted_nums[n // 2 - 1]
        upper_median = sorted_nums[n // 2]
        a_value = upper_median
        # 計算範圍內有多少個整數
        range_count = upper_median - lower_median + 1

    # 計算有多少個數字等於A
    equal_count = numbers.count(a_value)

    return a_value, equal_count, range_count


def main():
    """
    主程式: 讀入多組測資並輸出結果
    """
    while True:
        try:
            # 讀入第一個數字n，表示該組有n個數字
            n = int(input())

            # 當n = 0時，表示輸入結束
            if n == 0:
                break

            # 讀入n個數字
            numbers = list(map(int, input().split()))

            # 解決問題
            a, count, range_size = solve_password(numbers)

            # 輸出三個結果
            print(f"{a} {count} {range_size}")

        except EOFError:
            # 處理輸入結束的情況
            break


if __name__ == "__main__":
    main()
