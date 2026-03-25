"""
UVA 10056 - 輪流擲骰子遊戲的獲勝機率

問題描述:
--------
N個玩家輪流擲骰子，每次成功機率為p。當某玩家成功時獲勝，遊戲停止。
計算第i名玩家的獲勝機率。

核心演算法原理:
--------------
設第i名玩家獲勝的概率為 P(i)

第i名玩家獲勝意味著：
- 前面 (i-1) 個玩家全失敗
- 第i個玩家成功
- 或者前 n 個玩家都失敗（完成一輪），回到開始

使用幾何級數求和得到：
P(i) = p × (1-p)^(i-1) / (1 - (1-p)^n)

其中：
- p: 每次成功的機率
- (1-p)^(i-1): 前 i-1 個玩家都失敗的概率
- (1-p)^n: 一整輪 n 個玩家都失敗的概率

時間複雜度: O(N)
空間複雜度: O(1)
"""


def calculate_win_probability(n, p, i):
    """
    計算第i名玩家的獲勝機率

    參數:
    ----
    n: int 玩家數量
    p: float 每次成功的機率（0 ≤ p ≤ 1）
    i: int 要計算的玩家編號（1 ≤ i ≤ n）

    返回值:
    ------
    float 第i名玩家的獲勝機率

    演算法步驟:
    ---------
    1. 計算一次失敗的概率：q = 1 - p
    2. 計算第i個玩家之前都失敗的概率：q^(i-1)
    3. 計算一整輪都失敗的概率：q^n
    4. 使用公式：P(i) = p × q^(i-1) / (1 - q^n)
    """

    # 特殊情況：如果成功機率為0，沒有人能贏
    if p == 0:
        return 0.0

    # 特殊情況：如果成功機率為1，只有第一個玩家能贏
    if p == 1.0:
        if i == 1:
            return 1.0
        else:
            return 0.0

    # 計算失敗概率
    q = 1 - p

    # 計算一整輪都失敗的概率（用於歸一化）
    # (1 - p)^n 表示n個玩家全部失敗
    q_to_n = q**n

    # 計算第i個玩家之前都失敗的概率
    # (1 - p)^(i-1) 表示前i-1個玩家都失敗
    q_to_i_minus_1 = q ** (i - 1)

    # 使用公式計算概率
    # P(i) = p × (1-p)^(i-1) / (1 - (1-p)^n)
    numerator = p * q_to_i_minus_1
    denominator = 1 - q_to_n

    result = numerator / denominator

    return result


def read_and_process_input():
    """
    從標準輸入讀取測試資料並處理

    輸入格式:
    --------
    第一行: S 測試資料組數
    接下來S行，每行包含：
        N: 玩家數量
        p: 單次成功機率（浮點數）
        i: 要計算的玩家編號

    輸出:
    ----
    對每個測試資料，輸出第i名玩家的獲勝機率（精確到4位小數）
    """

    # 讀取測試資料組數
    s = int(input())

    # 處理每一組測試資料
    for _ in range(s):
        # 讀取 N, p, i
        parts = input().split()
        n = int(parts[0])
        p = float(parts[1])
        i = int(parts[2])

        # 計算並輸出結果
        result = calculate_win_probability(n, p, i)
        print(f"{result:.4f}")


if __name__ == "__main__":
    # 取消註解下一行來運行輸入處理
    # read_and_process_input()
    pass
