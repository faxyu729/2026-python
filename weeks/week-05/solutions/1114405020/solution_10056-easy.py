"""
UVA 10056 - 獲勝機率（簡單版本）

核心公式:
P(i) = p × (1-p)^(i-1) / (1 - (1-p)^n)

記憶方法:
1. 計算失敗概率 q = 1-p
2. 計算分子: p × q^(i-1)
3. 計算分母: 1 - q^n
4. 返回 分子/分母
"""


def calculate_win_probability(n, p, i):
    """計算第i名玩家的獲勝機率"""
    if p == 0:
        return 0.0
    if p == 1.0:
        return 1.0 if i == 1 else 0.0

    q = 1 - p
    return (p * q ** (i - 1)) / (1 - q**n)


# 主程式
if __name__ == "__main__":
    s = int(input())
    for _ in range(s):
        parts = input().split()
        n, p, i = int(parts[0]), float(parts[1]), int(parts[2])
        result = calculate_win_probability(n, p, i)
        print(f"{result:.4f}")
