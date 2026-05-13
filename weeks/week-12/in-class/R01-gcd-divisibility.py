# R01. GCD / LCM 與整除性（數論基礎）
# math.gcd / math.lcm / 整除判斷 / 數字位數和

import math

# ── GCD / LCM ────────────────────────────────────────────
print("=== GCD / LCM ===")
print(math.gcd(12, 8))          # 4
print(math.gcd(100, 75))        # 25
print(math.lcm(4, 6))           # 12   （Python 3.9+）

# 手動 Euclidean 算法（面試常考）
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

print(gcd(48, 18))              # 6

# ── 整除判斷 ─────────────────────────────────────────────
print("\n=== 整除判斷 ===")

def digit_sum(n: int) -> int:
    """計算各位數字之和（n 為非負整數）"""
    return sum(int(d) for d in str(n))

print(digit_sum(9))             # 9
print(digit_sum(18))            # 9
print(digit_sum(12345))         # 15

# 9 的倍數判斷：位數和也是 9 的倍數
def is_multiple_of_9(n: int) -> bool:
    return n % 9 == 0

# 遞迴縮減到個位數
def reduce_digit_sum(n: int) -> int:
    """反覆加總位數，直到只剩一位數"""
    s = str(n)
    while len(s) > 1:
        n = sum(int(d) for d in s)
        s = str(n)
    return n

print(reduce_digit_sum(9))      # 9
print(reduce_digit_sum(18))     # 9
print(reduce_digit_sum(999))    # 9
print(reduce_digit_sum(100))    # 1

# ── 9 的深度（UVA 10922）────────────────────────────────
def nine_degree(n: str) -> int:
    """計算 9-degree，n 為字串（避免大數溢位）"""
    degree = 0
    current = n
    while len(current) > 1:
        current = str(sum(int(d) for d in current))
        degree += 1
    return degree if current == "9" else -1   # -1 表示非 9 的倍數

print("\n=== 9-degree ===")
print(nine_degree("9"))         # 0  → 9 is a multiple of 9 with degree 0?
# 題目定義：至少要做一次加總，所以 9 本身 degree = 0 需確認
print(nine_degree("18"))        # 1  → 1+8=9
print(nine_degree("999"))       # 2  → 9+9+9=27 → 2+7=9
print(nine_degree("100"))       # -1 → 1+0+0=1，非 9 的倍數
