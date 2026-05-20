# -*- coding: utf-8 -*-
"""
UVA 11150 — 青蛙過獨木橋（簡易版本）

核心概念：
1. 如果每次跳的距離固定（S==T），只需要數「位置正好被跳到的石子」
2. 如果跳距有彈性（S<T），用「動態規劃」找最少石子數
3. 橋太長時用「路徑壓縮」把大間距縮短

解題口訣：「固定跳距直接算，彈性跳距用 DP，大間距就壓縮」
"""

def min_stones(L, S, T, stones):
    """
    計算青蛙最少會踩到幾顆石子。
    
    參數：
      L      — 橋的長度（終點位置）
      S      — 每次最少跳幾步
      T      — 每次最多跳幾步
      stones — 石子位置的串列
    
    回傳：最少踩到的石子數
    """
    # === 只保留橋上的石子，並由小到大排列 ===
    stones = sorted([s for s in stones if s <= L])
    
    # === 情況一：每次只能跳固定距離 ===
    # 這時候很簡單，只要檢查石子位置能不能被 S 整除
    if S == T:
        count = 0
        for s in stones:
            if s % S == 0:
                count += 1
        return count
    
    # === 情況二：跳距有彈性（S < T）===
    # 步驟 1：路徑壓縮（處理超長橋）
    # 把 [起點, 石子, 終點] 排成一列，大間距縮短
    positions = [0] + stones + [L]
    compressed = [0]
    for i in range(1, len(positions)):
        d = positions[i] - positions[i - 1]
        if d > T:
            # 如果間距比 T 大，把它縮到 T + 多出來的部分
            d = T + (d - T) % T
        compressed.append(compressed[-1] + d)
    
    new_L = compressed[-1]
    是石子 = set(compressed[1:-1])   # 壓縮後哪些位置有石子
    
    # 步驟 2：動態規劃（DP）
    # dp[i] = 「跳到位置 i 時，最少踩到幾顆石子」
    INF = float('inf')
    dp = [INF] * (new_L + T + 1)
    dp[0] = 0
    
    for i in range(new_L + 1):
        if dp[i] == INF:
            continue            # 到不了的位置，跳過
        for jump in range(S, T + 1):
            ni = i + jump       # 跳 jump 步後的位置
            if ni >= len(dp):
                continue
            加分 = 1 if ni in 是石子 else 0
            if dp[ni] > dp[i] + 加分:
                dp[ni] = dp[i] + 加分
    
    # 可以跳到或跳過 new_L，取最小值
    return min(dp[new_L:new_L + T + 1])


import unittest


class Test11150Easy(unittest.TestCase):
    """UVA 11150 簡易版測試"""

    def test_empty(self):
        """沒有石子 → 0"""
        self.assertEqual(min_stones(10, 1, 3, []), 0)

    def test_fixed_jump_hit(self):
        """固定跳 2 步，石子都在跳點上"""
        self.assertEqual(min_stones(10, 2, 2, [2, 4, 6, 8]), 4)

    def test_fixed_jump_miss(self):
        """固定跳 2 步，石子都不在跳點上"""
        self.assertEqual(min_stones(10, 2, 2, [1, 3, 5]), 0)

    def test_flexible_avoid(self):
        """跳距有彈性，可以避開石子"""
        self.assertEqual(min_stones(10, 2, 4, [5]), 0)

    def test_must_step(self):
        """兩顆石子相隔近，至少會踩到一顆"""
        self.assertEqual(min_stones(5, 1, 2, [2, 3]), 1)

    def test_huge_L(self):
        """超長橋 + 大間距壓縮"""
        self.assertEqual(min_stones(10**9, 2, 5, [100, 200]), 0)


if __name__ == "__main__":
    unittest.main()
