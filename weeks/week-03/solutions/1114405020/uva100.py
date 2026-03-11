# uva100.py
# 針對 UVA 100 (Collatz conjecture) 題目的簡易實作
#
# 此模組提供計算 Collatz 序列 cycle length 的函數，
# 以及給定區間時回傳其中的最大 cycle length。
#
# 所有註解以繁體中文撰寫，方便讀者理解演算法流程。

# 使用快取以避免重複計算，字典的 key 是整數 n，value 是其 cycle length。
_cache = {1: 1}


def cycle_length(n: int) -> int:
    """計算整數 n 的 Collatz cycle length。

    cycle length 定義為從 n 開始經由 Collatz 規則直到遇到 1
    所經過的步數總數（含 n 與 1）。

    此函式採用遞迴配合全域快取，
    對於之前計算過的數值可以直接回傳結果。

    Args:
        n: 正整數 (> 0)

    Returns:
        對應的 cycle length。
    """
    # 快取檢查
    if n in _cache:
        return _cache[n]

    # 根據 Collatz 規則前進到下一個數值
    if n % 2 == 0:
        next_n = n // 2
    else:
        next_n = 3 * n + 1

    # 使用遞迴計算，並將當前 n 的結果存入快取
    length = 1 + cycle_length(next_n)
    _cache[n] = length
    return length


def max_cycle_length(i: int, j: int) -> int:
    """計算介於 i 與 j（包含端點）之間整數的最大 cycle length。

    若 i > j，會自動交換以處理逆向區間。
    """
    # 確認起迄點順序，讓後續迴圈統一從小到大
    start, end = min(i, j), max(i, j)
    maxlen = 0
    # 對區間內每一個整數計算 cycle length，並取最大值
    for n in range(start, end + 1):
        current = cycle_length(n)  # 取得 n 的 cycle length
        if current > maxlen:
            maxlen = current
    return maxlen


def parse_input(line: str):
    """從單行字串解析出 i, j 這對整數。

    若該行為空白或無效，回傳 None，以供呼叫端忽略。
    支援多行輸入，避免因空白行而例外。
    """
    parts = line.strip().split()
    if not parts:  # 空行或只有空白
        return None
    i, j = map(int, parts)  # 直接轉型為整數對
    return i, j


def main():
    """從標準輸入讀取多行，每行印出 i j 最大 cycle length。

    範例輸入：
        1 10
        100 200
    輸出對應結果，直到 EOF。
    """
    import sys
    for line in sys.stdin:
        pair = parse_input(line)
        if pair is None:
            # 忽略空行或非數字行
            continue
        i, j = pair
        maxlen = max_cycle_length(i, j)
        # 輸出格式與原題目一致
        print(f"{i} {j} {maxlen}")


if __name__ == "__main__":
    # 當此模組直接執行時，啟動命令列介面
    main()
