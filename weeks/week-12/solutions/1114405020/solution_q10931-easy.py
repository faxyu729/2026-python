"""
UVA 10931 - 奇偶性校驗位（簡易版本）
最簡潔實現，易於記憶和理解

核心邏輯只需 10 行代碼
"""


# 簡易版本：最少代碼實現
def solve():
    """
    主函數：簡易版本
    邏輯：
    1. 讀取整數 n
    2. 轉換為二進位：bin(n) -> '0b...'
    3. 計算 1 的個數：binary_str.count('1')
    4. 計算奇偶性：ones_count % 2
    5. 輸出結果
    """
    while True:
        n = int(input())
        if n == 0:
            break
        
        # 轉換為二進位並計算 1 的個數
        binary = bin(n)[2:]  # 移除 '0b' 前綴
        ones = binary.count('1')  # 計算 1 的個數
        parity = ones % 2  # 計算奇偶性
        
        # 輸出結果
        print(f"The parity of {binary} is {parity} (mod 2).")


if __name__ == '__main__':
    solve()
