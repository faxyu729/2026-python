"""
UVA 10055 - 複合函數單調性（簡單版本）

核心邏輯很簡單:
- 減函數個數為偶數 → 增函數 (0)
- 減函數個數為奇數 → 減函數 (1)
"""


class MonotonFunction:
    """簡單版本的函數單調性管理器"""

    def __init__(self, n):
        """初始化 N 個函數（都是增函數）"""
        self.functions = [0] * n  # 0=增, 1=減

    def toggle(self, i):
        """反轉第 i 個函數"""
        self.functions[i - 1] = 1 - self.functions[i - 1]

    def query(self, l, r):
        """查詢複合函數的單調性"""
        # 計算減函數個數
        decreasing_count = sum(self.functions[l - 1 : r])
        # 返回奇偶性
        return decreasing_count % 2


# 主程式
if __name__ == "__main__":
    n, q = map(int, input().split())
    mf = MonotonFunction(n)

    for _ in range(q):
        operation = list(map(int, input().split()))
        v = operation[0]

        if v == 1:
            mf.toggle(operation[1])
        else:
            print(mf.query(operation[1], operation[2]))
