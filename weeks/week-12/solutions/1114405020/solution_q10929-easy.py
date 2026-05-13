"""
UVA 10929 - 簡易版本（約30行）
最簡潔的實現，邏輯清晰易於記憶
"""


def is_multiple_of_11(n):
    """檢查數字字符串是否為 11 的倍數"""
    # 計算奇數位和偶數位的數字之和
    odd_sum = sum(int(n[-(i+1)]) for i in range(0, len(n), 2))
    even_sum = sum(int(n[-(i+1)]) for i in range(1, len(n), 2))
    
    # 如果差值能被 11 整除，則是 11 的倍數
    return (odd_sum - even_sum) % 11 == 0


# 主程序
while True:
    n = input().strip()
    if n == "0":
        break
    
    if is_multiple_of_11(n):
        print(f"{n} is a multiple of 11.")
    else:
        print(f"{n} is not a multiple of 11.")
