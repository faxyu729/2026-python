"""
UVA 100 - 3n+1 (Collatz 序列) - 完整版解答程式

題目概述：
  給定兩個整數 i 和 j，計算介於 i 和 j 之間的所有整數所產生的 Collatz 序列中，
  最長的 cycle-length 是多少。

演算法說明：
  1. 對於每個數字 n，計算其 cycle-length：
     - 若 n = 1，cycle-length = 1
     - 若 n 為奇數，下一個數為 3*n + 1
     - 若 n 為偶數，下一個數為 n / 2
     - 重複直到 n = 1

  2. 在區間 [min(i, j), max(i, j)] 內，找到最大的 cycle-length。

  3. 使用記憶化（快取）來避免重複計算相同數字的 cycle-length。

時間複雜度：O((j-i) * log(n))，其中 n 為區間內最大的數。
空間複雜度：O(max_value)，用於存儲快取。
"""

# 全域快取字典，用於存儲已計算過的 cycle-length，避免重複計算
_cycle_cache = {1: 1}


def calculate_cycle_length(n):
    """
    計算單個數字 n 的 Collatz 序列長度（cycle-length）。

    參數：
        n (int)：要計算 cycle-length 的正整數。

    返回值：
        int：從 n 開始到 1 的步數（包含 n 和 1）。

    範例：
        calculate_cycle_length(1) → 1
        calculate_cycle_length(22) → 16
    """
    # 若已在快取中，直接返回快取的結果
    if n in _cycle_cache:
        return _cycle_cache[n]

    # 保存原始的 n 值，以便之後儲存到快取中
    original_n = n

    # 遞迴計算：根據奇偶性調整 n，並加上 1（表示當前步驟）
    if n % 2 == 1:
        # n 為奇數：n = 3*n + 1
        _cycle_cache[original_n] = 1 + calculate_cycle_length(3 * n + 1)
    else:
        # n 為偶數：n = n / 2
        _cycle_cache[original_n] = 1 + calculate_cycle_length(n // 2)

    return _cycle_cache[original_n]


def find_max_cycle_length(i, j):
    """
    在區間 [min(i, j), max(i, j)] 內，找到最大的 cycle-length。

    參數：
        i (int)：區間的一端（0 < i < 1,000,000）。
        j (int)：區間的另一端（0 < j < 1,000,000）。

    返回值：
        int：區間內所有數字的最大 cycle-length。

    說明：
        函式會自動處理 i > j 的情況，即會先將 i 和 j 的大小關係正規化。

    範例：
        find_max_cycle_length(1, 10) → 20
        find_max_cycle_length(100, 200) → 125
    """
    # 正規化區間，確保 min_val <= max_val
    min_val = min(i, j)
    max_val = max(i, j)

    # 在區間內遍歷，計算每個數的 cycle-length 並記錄最大值
    max_length = 0
    for num in range(min_val, max_val + 1):
        length = calculate_cycle_length(num)
        max_length = max(max_length, length)

    return max_length


def main():
    """
    主程式：讀取輸入並輸出結果。

    輸入格式：
        每行包含兩個整數 i 和 j。
        當輸入 EOF 時結束。

    輸出格式：
        對每行輸入，輸出 "i j max_cycle_length"。
    """
    try:
        while True:
            line = input().strip()
            if not line:
                break

            # 解析輸入的兩個整數
            i, j = map(int, line.split())

            # 計算並輸出結果
            max_length = find_max_cycle_length(i, j)
            print(f"{i} {j} {max_length}")

    except EOFError:
        # 當遇到 EOF（檔案結束）時，正常結束程式
        pass


if __name__ == "__main__":
    main()
