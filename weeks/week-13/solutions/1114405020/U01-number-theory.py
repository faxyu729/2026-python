# U01. 數論整合應用
# 整合 GCD / 線性方程 / 大數整除，對應 Week 12 解題題目

import math      # 數學函式庫，提供 gcd（最大公因數）等函式
import sys       # 系統函式庫（本程式未直接使用，保留供擴充）

# ── 應用 1：Beat the Spread!（UVA 10812）────────────────
# 題目：給定兩隊比賽分數的「總和 S」與「差距 D」，求兩隊各自得分。
# 數學推導：
#   設高分 = h，低分 = l，則：
#     h + l = S
#     h - l = D
#   解聯立方程式得：
#     h = (S + D) / 2
#     l = (S - D) / 2
# 限制條件：
#   1. (S + D) 必須為偶數（否則 h 不是整數）
#   2. h >= l >= 0（比分不能為負）

def beat_the_spread(s: int, d: int):
    """
    根據總分 s 與分差 d 計算兩隊各自得分。
    
    參數：
        s : int — 兩隊分數總和
        d : int — 兩隊分數差距
    
    回傳值：
        (high, low) : tuple — (高分, 低分)
        None — 無解（不符合整數或非負條件）
    
    條件：
        - (s + d) 必須為偶數，確保 high 為整數
        - low >= 0，確保低分不為負數
    """
    # 若 (s+d) 是奇數，代表無法整除 2，無整數解
    if (s + d) % 2 != 0:
        return None
    # 整數除法計算高分（無條件捨去，但因已確認偶數，結果就是正確整數）
    high = (s + d) // 2
    # 整數除法計算低分
    low  = (s - d) // 2
    # 低分若為負數，不符合比賽得分規則，視為無解
    if low < 0:
        return None
    # 回傳 (高分, 低分)
    return (high, low)


# 測試 Beat the Spread! 函式
# 測資格式：(總和 S, 差距 D)
print("=== Beat the Spread! ===")
tests = [(40, 20), (20, 40), (10, 10), (10, 11)]   # (S, D) 測試案例
for s, d in tests:
    result = beat_the_spread(s, d)                  # 呼叫函式求解
    if result:
        # 有解：印出兩隊得分
        print(f"S={s} D={d}  → {result[0]} {result[1]}")
    else:
        # 無解：印出 impossible
        print(f"S={s} D={d}  → impossible")

# ── 應用 2：2 the 9s（UVA 10922）────────────────────────
# 題目：判斷一個「大數」（以字串表示）是否為 9 的倍數，
#       並且計算其「9 度數」（nine degree）。
#
# 原理：
#   一個數是 9 的倍數 ↔ 其各位數字之和也是 9 的倍數。
#   「9 度數」是指反覆計算各位數之和，直到剩下一位數所需的次數。
#   例如：999 → 9+9+9=27 → 2+7=9，深度為 2。
#
# 注意：因為數字可能非常大（如 1000 位數），不能用 int 儲存，
#       必須以字串處理。

def nine_degree(n_str: str):
    """
    判斷大數是否為 9 的倍數，並計算其 9 度數（反覆求各位數和的次數）。
    
    參數：
        n_str : str — 以字串表示的大整數
    
    回傳值：
        (True, degree) — 是 9 的倍數，degree 為 9 度數
        (False, -1)    — 不是 9 的倍數
    
    演算法：
        1. 將 current 初始化為輸入字串
        2. degree 從 0 開始計數
        3. 只要 current 的位數 > 1，或 (degree==0 且位數==1)：
           a. 計算各位數字總和 s
           b. 將 s 轉為字串作為新的 current
           c. degree 加 1
           d. 若 current 只剩一位數則跳出
        4. 最後若 current == "9" 表示是 9 的倍數
    """
    current = n_str        # current 儲存當前要處理的數字字串
    degree = 0             # 記錄計算深度（反覆求和的次數）
    
    # 迴圈條件：
    # - 若位數 > 1，需要繼續計算各位數和
    # - 若位數 == 1 且 degree == 0（第一次進入），也需要檢查
    while len(current) > 1 or (degree == 0 and len(current) == 1):
        # 使用生成式將每個字元轉為 int 並加總
        s = sum(int(c) for c in current)
        current = str(s)   # 將總和轉回字串，準備下一輪計算
        degree += 1        # 深度加 1
        
        # 若 current 已剩一位數，提前跳出迴圈
        if len(current) == 1:
            break
    
    # 最終若剩下的是 "9"，代表原數是 9 的倍數
    if current == "9":
        return True, degree
    # 否則不是 9 的倍數
    return False, -1


# 測試 2 the 9s 函式
print("\n=== 2 the 9s ===")
cases = ["9", "18", "999", "100", "729"]   # 測試案例
for n in cases:
    is_mult, deg = nine_degree(n)           # 呼叫函式判斷
    if is_mult:
        # 是 9 的倍數，印出深度
        print(f"9-degree of {n} is {deg}.")
    else:
        # 不是 9 的倍數
        print(f"{n} is not a multiple of 9.")

# ── 應用 3：Can You Solve It?（UVA 10642）────────────────
# 題目：給定一個螺旋座標系統，計算從 (x1,y1) 到 (x2,y2) 需要多少步。
#
# 座標系統說明：
#   座標以螺旋方式排列，從原點 (0,0) 開始向外延伸。
#   每個整數點座標 (x,y) 都有一個唯一的編號（從 0 開始）。
#   步數 = 目的地編號 - 起點編號的絕對值。
#
# 位置公式推導：
#   若 x >= y（在對角線下方或對角線上）：
#     位置 = x * x + x + y
#   若 x < y（在對角線上方）：
#     位置 = y * y + x
#
# 這兩條公式分別涵蓋了螺旋中「橫向」與「縱向」的排列規律。

def position(x, y):
    """
    計算座標 (x,y) 在螺旋系統中的位置編號（從 0 開始）。
    
    參數：
        x : int — x 座標（非負整數）
        y : int — y 座標（非負整數）
    
    回傳值：
        int — 該座標的位置編號
    
    公式：
        if x >= y:  position = x² + x + y
        if x <  y:  position = y² + x
    """
    if x >= y:
        # 在對角線（含）下方：以 x 為主軸計算
        return x * x + x + y
    else:
        # 在對角線上方：以 y 為主軸計算
        return y * y + x

def steps(x1, y1, x2, y2):
    """
    計算從 (x1,y1) 到 (x2,y2) 所需的步數。
    
    參數：
        x1, y1 : int — 起點座標
        x2, y2 : int — 終點座標
    
    回傳值：
        int — 所需的步數（= 兩點位置編號差的絕對值）
    
    原理：
        因為螺旋編號是連續的整數，所以步數 = |位置2 - 位置1|
    """
    # 計算兩點位置編號的差距（取絕對值即為步數）
    return abs(position(x2, y2) - position(x1, y1))


# 測試 Can You Solve It? 函式
print("\n=== Can You Solve It? ===")
# 測試案例格式：(x1, y1, x2, y2)
cases = [(0, 3, 3, 0), (0, 0, 2, 2), (1, 1, 2, 3)]
for x1, y1, x2, y2 in cases:
    s = steps(x1, y1, x2, y2)     # 計算步數
    # 印出結果
    print(f"({x1},{y1}) → ({x2},{y2})  步數 = {s}")
