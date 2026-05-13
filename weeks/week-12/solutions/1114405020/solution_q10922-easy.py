"""
UVA 10922 - 2 the 9s 簡易版本（~30 行）

邏輯清晰，易於記憶和理解的實現
"""


def sum_digits(n):
    """計算各位數字之和"""
    return sum(int(d) for d in str(n))


def is_multiple_of_9(n):
    """判斷是否為 9 的倍數：各位數字之和被 9 整除"""
    return sum_digits(n) % 9 == 0


def calculate_9_degree(n):
    """計算 9 的深度：重複計算數字之和直到得到 9"""
    depth = 0
    while n != 9:
        n = sum_digits(n)
        depth += 1
    return max(depth, 1)


# 主程式
while True:
    n = int(input())
    if n == 0:
        break
    
    if is_multiple_of_9(n):
        degree = calculate_9_degree(n)
        print(f"9-degree of {n} is {degree}.")
    else:
        print(f"{n} is not a multiple of 9.")
