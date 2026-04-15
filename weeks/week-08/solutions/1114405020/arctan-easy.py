"""
反正切計算 π (Arctan) - 簡易版本

簡化說明：
使用數學公式直接計算 arctan 分解
"""


def find_arctan_decomposition_easy(a):
    """
    找出 arctan(1/a) = arctan(1/b) + arctan(1/c) 中 b+c 的最小值

    簡易思路：
    根據 arctan 相加公式：
    arctan(1/b) + arctan(1/c) = arctan((1/b + 1/c)/(1 - 1/(bc)))
                               = arctan((b+c)/(bc-1))

    要使其等於 arctan(1/a)，需要：
    (b+c)/(bc-1) = 1/a

    交叉相乘得：
    a(b+c) = bc - 1
    ab + ac = bc - 1
    bc - ab - ac - 1 = 0

    令 c 為變數，可得：
    b = (ac + 1)/(c - a)

    簡單做法：
    遍歷所有可能的 c 值（c > a），檢查 b 是否為正整數
    選擇使 b+c 最小的組合
    """

    # 特殊情況：a = 1
    # 已知：arctan(1) = arctan(1/2) + arctan(1/3)
    if a == 1:
        return 2, 3

    # 初始化最佳結果
    best_sum = float("inf")
    best_b = None
    best_c = None

    # 搜索 c 的可能值
    # c 必須大於 a（保證分母 c-a > 0）
    for c in range(a + 1, a * a + 1):
        # 計算對應的 b
        numerator = a * c + 1
        denominator = c - a

        # 檢查 b 是否為正整數
        if numerator % denominator == 0:
            b = numerator // denominator

            if b > 0:
                current_sum = b + c

                # 找最小的和
                if current_sum < best_sum:
                    best_sum = current_sum
                    best_b = b
                    best_c = c

    return best_b, best_c


# 簡易測試
if __name__ == "__main__":
    print("=== 反正切計算 π 簡易版本測試 ===\n")

    print("公式：arctan(1/a) = arctan(1/b) + arctan(1/c)")
    print("求：使 b+c 最小的 (b, c) 組合\n")

    # 測試多個 a 值
    test_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for a in test_values:
        b, c = find_arctan_decomposition_easy(a)

        if b is not None and c is not None:
            print(f"a = {a:2d}:  b = {b:3d},  c = {c:3d},  b+c = {b + c:3d}")
        else:
            print(f"a = {a:2d}:  無解")

    print("\n" + "=" * 50)
    print("結果說明：")
    print("- 公式基於 arctan 相加公式推導")
    print("- 搜索範圍：c 從 a+1 到 a的平方")
    print("- 返回使 b+c 最小的解")
    print("- 特殊處理：a=1 時直接返回 (2, 3)")
