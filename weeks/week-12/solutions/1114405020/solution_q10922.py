"""
UVA 10922 - 2 the 9s 標準版本

問題描述：
----------
輸入一個正整數，判斷是否為 9 的倍數。
如果是，計算其 9 的深度（9-degree）。

9 的深度定義：
- 對於 9 的倍數，計算各位數字之和
- 重複此過程直到得到數字 9
- 計數重複的次數即為 9 的深度

例子：
- 9: 深度 = 1
- 18: 1+8=9, 深度 = 1
- 99: 9+9=18, 1+8=9, 深度 = 2
- 999: 9+9+9=27, 2+7=9, 深度 = 2

輸出格式：
- 非倍數：[X] is not a multiple of 9.
- 是倍數：9-degree of [X] is [Y].

輸入 0 時停止程式。
"""


def sum_digits(n):
    """
    計算一個數字的各位數字之和
    
    參數：
        n (int): 輸入的整數
    
    回傳：
        int: 各位數字的總和
    
    例子：
        sum_digits(123) = 1 + 2 + 3 = 6
        sum_digits(18) = 1 + 8 = 9
        sum_digits(9) = 9
    """
    total = 0
    while n > 0:
        total += n % 10  # 取最後一位數字，加到總和
        n //= 10         # 移除最後一位數字
    return total


def is_multiple_of_9(n):
    """
    判斷一個數字是否為 9 的倍數
    
    數學原理：
    - 一個數是 9 的倍數，當且僅當其各位數字之和是 9 的倍數
    - 這是因為 10 ≡ 1 (mod 9)，所以任何數 mod 9 等於其數字之和 mod 9
    
    參數：
        n (int): 輸入的整數
    
    回傳：
        bool: True 表示是 9 的倍數，False 表示不是
    
    例子：
        is_multiple_of_9(9) = True
        is_multiple_of_9(18) = True
        is_multiple_of_9(10) = False
    """
    digit_sum = sum_digits(n)
    return digit_sum % 9 == 0


def calculate_9_degree(n):
    """
    計算一個數的 9 的深度
    
    演算法：
    1. 重複計算各位數字之和直到得到 9
    2. 計數重複的次數（如果原本已是 9，深度為 1）
    
    參數：
        n (int): 必須是 9 的倍數的整數
    
    回傳：
        int: 9 的深度
    
    例子：
        calculate_9_degree(9) = 1
        calculate_9_degree(18) = 1  (1+8=9)
        calculate_9_degree(99) = 2  (9+9=18, 1+8=9)
        calculate_9_degree(999) = 2 (9+9+9=27, 2+7=9)
    """
    depth = 0
    
    # 重複計算各位數字之和直到得到 9
    while n != 9:
        n = sum_digits(n)  # 計算各位數字之和
        depth += 1         # 增加深度計數
    
    # 如果原本已是 9（即沒有進入迴圈），深度為 1
    # 否則深度就是進行的計算次數
    return max(depth, 1)


def solve_uva_10922():
    """
    主程式：解決 UVA 10922 問題
    
    流程：
    1. 不斷讀取輸入
    2. 如果輸入是 0，停止程式
    3. 判斷是否為 9 的倍數
    4. 如果是，計算並輸出 9 的深度
    5. 如果不是，輸出相應的訊息
    """
    while True:
        # 讀取輸入
        try:
            n = int(input())
        except EOFError:
            # 處理 EOF（程式結束）
            break
        
        # 輸入 0 時停止
        if n == 0:
            break
        
        # 判斷是否為 9 的倍數
        if is_multiple_of_9(n):
            # 計算 9 的深度
            degree = calculate_9_degree(n)
            print(f"9-degree of {n} is {degree}.")
        else:
            # 輸出不是 9 的倍數的訊息
            print(f"{n} is not a multiple of 9.")


if __name__ == "__main__":
    solve_uva_10922()
