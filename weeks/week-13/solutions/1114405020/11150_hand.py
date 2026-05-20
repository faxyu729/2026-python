# -*- coding: utf-8 -*-
"""
UVA 11150 — 青蛙過獨木橋（手打程式）

題目：青蛙從橋起點 0 跳到終點 L，每次可跳 S~T 個單位。
      橋上有 M 個石子，目標是算出「最少踩到石子的數量」。

技巧：L 可達 10^9，但只有 ≤100 顆石子，需「路徑壓縮」。
"""

def min_stones(L, S, T, stones):
    """計算青蛙過河最少需要踩到的石子數"""
    stones = sorted([s for s in stones if s <= L])

    if S == T:
        return sum(1 for s in stones if s % S == 0)

    positions = [0] + stones + [L]
    compressed = [0]
    for i in range(1, len(positions)):
        dist = positions[i] - positions[i - 1]
        if dist > T:
            dist = T + (dist - T) % T
        compressed.append(compressed[-1] + dist)

    new_L = compressed[-1]
    stone_set = set(compressed[1:-1])

    INF = float('inf')
    size = new_L + T + 1
    dp = [INF] * size
    dp[0] = 0

    for i in range(new_L + 1):
        if dp[i] == INF:
            continue
        for jump in range(S, T + 1):
            ni = i + jump
            if ni < size:
                add = 1 if ni in stone_set else 0
                if dp[ni] > dp[i] + add:
                    dp[ni] = dp[i] + add

    return min(dp[new_L:new_L + T + 1])


def solve_one_case(L, S, T, stones):
    """處理一組測試資料，回傳最少石子數"""
    return min_stones(L, S, T, stones)


def main():
    """主程式：從標準輸入讀取資料並輸出結果"""
    import sys
    data = sys.stdin.read().strip().splitlines()
    idx = 0
    while idx < len(data):
        line = data[idx].strip()
        if not line:
            idx += 1
            continue
        L = int(line)
        idx += 1
        S, T, M = map(int, data[idx].strip().split())
        idx += 1
        stones = list(map(int, data[idx].strip().split()))
        idx += 1
        print(solve_one_case(L, S, T, stones))


if __name__ == "__main__":
    main()
