# uva100_easy.py
# 比較簡單、好記版本的 UVA 100 解法
#
# 此檔案提供與 uva100.py 相同功能，但用更直觀的迴圈實作
# 並略去快取與遞迴，適合初學者快速理解 Collatz 過程。


def cycle_length_easy(n: int) -> int:
    """計算整數 n 的 Collatz cycle length。

    此簡化版採用最直接的迴圈式演算法：
    1. 初始化長度為 1（因為包括起始的 n 本身）。
    2. 當 n 不是 1 時，不斷重複：
       - 若 n 為偶數，將 n 設為 n/2。
       - 若 n 為奇數，將 n 設為 3n+1。
       - 每次變動後，長度加 1。
    3. 直到 n 等於 1 後回傳長度。

    這個版本不使用遞迴或全域快取，便於初學者一步一步理解
    Collatz 序列的變化過程。
    """
    length = 1  # 計算步數，至少為 1
    # 迴圈執行直到遇到 1
    while n != 1:
        # 判斷奇偶更新 n
        if n % 2 == 0:
            n //= 2  # 偶數直接除以 2
        else:
            n = 3 * n + 1  # 奇數則乘 3 加 1
        length += 1  # 每次規則應用視為一步
    return length


def max_cycle_length_easy(i: int, j: int) -> int:
    """計算區間 [i, j] 的最大 cycle length（包含端點）。

    步驟：
    * 先確保 start <= end，以支援輸入 i>j 的情況。
    * 依序對每個數字計算 cycle length，並追蹤最大值。
    * 回傳所發現的最大 cycle length。
    """
    # 正規化區間順序
    start, end = min(i, j), max(i, j)
    maxlen = 0
    # 逐一計算每個數字的 cycle length
    for num in range(start, end + 1):
        length = cycle_length_easy(num)
        # 若本次大於先前紀錄，更新最大值
        if length > maxlen:
            maxlen = length
    return maxlen


def parse_input(line: str):
    """解析輸入行並回傳數字對，空行則回傳 None。

    讀取一行文字並用空白切割成元件。
    若該行不包含任何數字，回傳 None；否則回傳 i, j 的 tuple。
    """
    parts = line.strip().split()
    if not parts:  # 防止空行或只有空白
        return None
    # map 回傳一個 map 物件，可直接拆包給變數
    return map(int, parts)


def main():
    """命令列介面：讀取 stdin 多行，並列印結果。

    每行格式為「i j」，輸出「i j 最大cycle-length」。
    例如輸入：
        1 10
        100 200
    將依序輸出對應計算結果，直到遇到 EOF（結束輸入）。
    """
    import sys
    for line in sys.stdin:
        pair = parse_input(line)
        if pair is None:  # 忽略空白行
            continue
        i, j = pair
        print(f"{i} {j} {max_cycle_length_easy(i,j)}")


if __name__ == "__main__":
    main()
