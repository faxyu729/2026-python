"""
UVA 100 - 3n+1 (Collatz 序列) - 簡單易記版本

這是針對 UVA 100 問題的簡化版本，專為容易記憶與手寫而設計。
在競賽環境（CPE 或其他程式設計競賽）中，通常需要在 2-3 分鐘內手寫完整程式，
所以這個版本採用最直接、最簡潔的方式來實現。

核心思想：
  1. 計算 cycle-length：給定 n，根據規則重複操作直到 n = 1。
  2. 區間查詢：在 [i, j] 的所有數字中，找出最大的 cycle-length。
"""

# 全域快取：存儲已計算過的 cycle-length，避免重複計算
cache = {1: 1}


def cycle_length(n):
    """
    計算數字 n 的 Collatz 序列長度。

    最核心的計算邏輯，直接對應題目的演算法：
    - 如果 n = 1，長度為 1
    - 如果 n 為奇數，n 變成 3*n + 1
    - 如果 n 為偶數，n 變成 n / 2
    - 重複直到 n = 1

    參數：
        n: 要計算的數字

    返回值：
        從 n 開始到 1 的步數（包含起點和終點）
    """
    # 檢查是否已經在快取中
    if n in cache:
        return cache[n]

    # 保存原始值，稍後用於存入快取
    original = n

    # 遞迴計算：根據奇偶性調整 n，並加上 1
    if n % 2 == 1:
        # n 為奇數：3*n + 1
        cache[original] = 1 + cycle_length(3 * n + 1)
    else:
        # n 為偶數：n / 2
        cache[original] = 1 + cycle_length(n // 2)

    return cache[original]


def max_cycle_in_range(i, j):
    """
    找出區間 [i, j] 內最大的 cycle-length。

    參數：
        i, j: 區間的兩端（順序無關，函式會自動處理）

    返回值：
        區間內所有數字的最大 cycle-length
    """
    # 確保 low <= high（處理輸入順序反序的情況）
    low = min(i, j)
    high = max(i, j)

    # 在區間內遍歷，計算最大值
    max_len = 0
    for num in range(low, high + 1):
        length = cycle_length(num)
        max_len = max(max_len, length)

    return max_len


# 主程式入口
if __name__ == "__main__":
    """
    讀取輸入並處理。

    輸入：每行一對整數 i j
    輸出：每行輸出 "i j max_cycle_length"

    範例：
        輸入：
            1 10
            100 200
        輸出：
            1 10 20
            100 200 125
    """
    import sys

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # 解析輸入
        i, j = map(int, line.split())

        # 計算結果
        result = max_cycle_in_range(i, j)

        # 輸出結果（保持原始順序 i, j）
        print(f"{i} {j} {result}")
