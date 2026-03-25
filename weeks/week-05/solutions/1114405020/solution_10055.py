"""
UVA 10055 - 複合函數的單調性判斷

問題描述:
--------
有N個函數，初始全為增函數。可以反轉某函數的增減性，或查詢L到R
的函數複合後的單調性。

核心演算法原理:
--------------
複合函數 F(x) = f_L(f_{L+1}(...f_R(x)...)) 的單調性取決於
組成它的所有函數中「減函數」的個數：

1. 減函數個數為偶數時：複合函數是增函數（輸出0）
2. 減函數個數為奇數時：複合函數是減函數（輸出1）

數學原理:
--------
- 增 ∘ 增 = 增 (0 + 0 = 0 mod 2)
- 增 ∘ 減 = 減 (0 + 1 = 1 mod 2)
- 減 ∘ 增 = 減 (1 + 0 = 1 mod 2)
- 減 ∘ 減 = 增 (1 + 1 = 0 mod 2)

時間複雜度: O(1) 每次操作
空間複雜度: O(N) 存儲N個函數的狀態
"""


class MonotonFunction:
    """用於管理和查詢複合函數單調性的類"""

    def __init__(self, n):
        """
        初始化 N 個函數

        參數:
        ----
        n: int 函數個數

        說明:
        ----
        所有函數初始為增函數，用 0 表示增函數，1 表示減函數
        """
        # 存儲 N 個函數的增減性
        # functions[i] = 0 表示 f_{i+1} 是增函數
        # functions[i] = 1 表示 f_{i+1} 是減函數
        # 注意：使用 0-based 索引，但函數編號是 1-based
        self.functions = [0] * n
        self.n = n

    def toggle(self, i):
        """
        反轉第 i 個函數的增減性

        參數:
        ----
        i: int 函數編號（1-based，從1到N）

        說明:
        ----
        將 f_i 的增減性反轉：
        - 增函數 (0) 變成減函數 (1)
        - 減函數 (1) 變成增函數 (0)
        """
        # 轉換為 0-based 索引
        idx = i - 1
        # 反轉：0 變 1，1 變 0
        self.functions[idx] = 1 - self.functions[idx]

    def query(self, l, r):
        """
        查詢複合函數 F(x) = f_L(f_{L+1}(...f_R(x)...)) 的單調性

        參數:
        ----
        l: int 起始函數編號（1-based）
        r: int 終止函數編號（1-based）

        返回值:
        ------
        int 複合函數的單調性
        - 0：增函數
        - 1：減函數

        演算法步驟:
        ---------
        1. 計算 [l, r] 範圍內減函數的個數
        2. 根據個數的奇偶性判斷結果：
           - 偶數個減函數 → 增函數 (0)
           - 奇數個減函數 → 減函數 (1)
        """
        # 計數減函數的個數
        decreasing_count = 0

        # 遍歷 [l, r] 範圍內的所有函數（1-based）
        for i in range(l, r + 1):
            # 轉換為 0-based 索引
            idx = i - 1
            # 如果是減函數，計數加 1
            if self.functions[idx] == 1:
                decreasing_count += 1

        # 根據減函數個數的奇偶性返回結果
        # 減函數個數 % 2：
        # - 偶數 (0) → 增函數，返回 0
        # - 奇數 (1) → 減函數，返回 1
        return decreasing_count % 2


def read_and_process_input():
    """
    從標準輸入讀取測試資料並處理

    輸入格式:
    --------
    第一行: N Q (N個函數，Q個操作)
    接下來Q行，每行：
        v = 1: 反轉操作，後跟整數 i (1 <= i <= N)
        v = 2: 查詢操作，後跟整數 L, R (1 <= L <= R <= N)

    輸出:
    ----
    對每個查詢操作，輸出結果（0 或 1）
    """
    # 讀取 N 和 Q
    n, q = map(int, input().split())

    # 創建函數管理器
    mf = MonotonFunction(n)

    # 處理每個操作
    for _ in range(q):
        # 讀取操作類型
        operation = list(map(int, input().split()))
        v = operation[0]

        if v == 1:
            # 反轉操作
            i = operation[1]
            mf.toggle(i)
        else:  # v == 2
            # 查詢操作
            l = operation[1]
            r = operation[2]
            result = mf.query(l, r)
            print(result)


if __name__ == "__main__":
    # 取消註解下一行來運行輸入處理
    # read_and_process_input()
    pass
