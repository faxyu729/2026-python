"""
UVA 10929 - Let's Play Euclid
標準版本解決方案

11 的倍數判斷規則：
一個數是 11 的倍數，當且僅當其奇數位上的數字之和減去偶數位上的數字之和能被 11 整除。
位數從右到左編號：個位是第 1 位（奇數位），十位是第 2 位（偶數位），依此類推。

例如：121 的分析
- 個位（第 1 位，奇數位）：1
- 十位（第 2 位，偶數位）：2
- 百位（第 3 位，奇數位）：1
- 奇數位之和：1 + 1 = 2
- 偶數位之和：2
- 差值：2 - 2 = 0
- 0 % 11 == 0，所以 121 是 11 的倍數
"""


def is_multiple_of_11(n):
    """
    判斷一個數字字符串是否是 11 的倍數
    
    參數：
        n (str): 表示數字的字符串
    
    返回值：
        bool: 如果是 11 的倍數返回 True，否則返回 False
    
    算法：
        1. 從右到左遍歷每一位數字
        2. 計算奇數位（第 1、3、5... 位）的和
        3. 計算偶數位（第 2、4、6... 位）的和
        4. 檢查 (奇數位之和 - 偶數位之和) 是否能被 11 整除
    """
    # 奇數位之和（從右到左第 1、3、5... 位）
    odd_sum = 0
    # 偶數位之和（從右到左第 2、4、6... 位）
    even_sum = 0
    
    # 從右到左遍歷每一位
    # enumerate 會從左到右計數，所以使用 reversed 來反轉字符串
    for position, digit in enumerate(reversed(n), start=1):
        digit_value = int(digit)
        
        # 位置從 1 開始計數
        if position % 2 == 1:  # 奇數位（第 1、3、5... 位）
            odd_sum += digit_value
        else:  # 偶數位（第 2、4、6... 位）
            even_sum += digit_value
    
    # 計算差值，檢查是否能被 11 整除
    difference = odd_sum - even_sum
    return difference % 11 == 0


def main():
    """
    主程序：讀取輸入並判斷是否為 11 的倍數
    
    輸入：
        - 多行數字（每行一個數字字符串）
        - 輸入 0 時停止
    
    輸出：
        - 對每個數字輸出 "[N] is a multiple of 11." 或 "[N] is not a multiple of 11."
    """
    while True:
        n = input().strip()
        
        # 輸入 0 時停止
        if n == "0":
            break
        
        # 判斷是否為 11 的倍數
        if is_multiple_of_11(n):
            print(f"{n} is a multiple of 11.")
        else:
            print(f"{n} is not a multiple of 11.")


if __name__ == "__main__":
    main()
