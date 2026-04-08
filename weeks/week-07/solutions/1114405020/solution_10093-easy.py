#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 10093 - 炮兵部隊部署問題 簡化版本

=== 核心思路 ===
使用「動態規劃 + 位元遮罩」
- 由於 M ≤ 10，可以用位元遮罩表示每行的炮兵位置
- DP狀態：dp[行][前一行遮罩][當前行遮罩] = 最大炮兵數
- 轉移時檢查：同行無衝突 + 行間無衝突

=== 攻擊範圍 ===
- 同一行中，距離≤2的炮兵會互相攻擊
- 同一列中，距離≤2的炮兵會互相攻擊
- 因此：距離>2的位置才能同時放置炮兵
"""

from typing import List


def count_bits(mask: int) -> int:
    """計算mask中1的個數。"""
    count = 0
    while mask:
        mask &= mask - 1
        count += 1
    return count


def is_valid_row(mask: int, m: int) -> bool:
    """
    檢查單行部署是否合法。

    合法條件：同行任意兩個炮兵距離 > 2

    例子：
    m=5, mask=0b10100 (第2,4列)
    距離 = 4-2 = 2，距離≤2，返回False（不合法）

    m=5, mask=0b10001 (第0,4列)
    距離 = 4-0 = 4，距離>2，返回True（合法）
    """
    positions = []
    for col in range(m):
        if mask & (1 << col):
            positions.append(col)

    # 檢查任意兩個位置距離是否≤2
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if positions[j] - positions[i] <= 2:
                return False
    return True


def can_coexist(mask1: int, mask2: int) -> bool:
    """
    檢查兩個相鄰行是否相容。

    相鄰行距離為1，同一列的炮兵會互相攻擊。
    因此：mask1 & mask2 必須為0

    例子：
    mask1=0b10100, mask2=0b01010
    mask1 & mask2 = 0b00000 → 相容（返回True）
    """
    return (mask1 & mask2) == 0


def solve_artillery(n: int, m: int, grid: List[str]) -> int:
    """
    主求解函數。

    演算法流程：
    1. 找出所有合法行遮罩
    2. 用DP跟蹤最大炮兵數
    3. 轉移時檢查：
       - 同行無衝突（is_valid_row）
       - 行間無衝突（can_coexist + 距離為2的行）
    """

    # ===== 預處理：找出所有合法遮罩 =====
    valid_masks = []
    for mask in range(1 << m):
        if is_valid_row(mask, m):
            valid_masks.append(mask)

    # ===== 初始化：處理第0行 =====
    prev_dp = {}  # (mask0) -> max_count

    for mask0 in valid_masks:
        # 檢查mask0的所有位置是否都在平原上
        valid = True
        for col in range(m):
            if (mask0 & (1 << col)) and grid[0][col] != "P":
                valid = False
                break
        if valid:
            prev_dp[mask0] = count_bits(mask0)

    if n == 1:
        return max(prev_dp.values()) if prev_dp else 0

    # ===== 轉移：逐行處理 =====
    # 需要跟蹤前兩行的遮罩，以檢查距離為2的衝突

    # 處理第1行
    curr_dp = {}  # (mask0, mask1) -> max_count

    for mask0, count0 in prev_dp.items():
        for mask1 in valid_masks:
            # 檢查mask1的位置是否在平原上
            valid = True
            for col in range(m):
                if (mask1 & (1 << col)) and grid[1][col] != "P":
                    valid = False
                    break
            if not valid:
                continue

            # 檢查mask0和mask1相容
            if not can_coexist(mask0, mask1):
                continue

            key = (mask0, mask1)
            count1 = count_bits(mask1)
            if key not in curr_dp:
                curr_dp[key] = count0 + count1
            else:
                curr_dp[key] = max(curr_dp[key], count0 + count1)

    if n == 2:
        return max(curr_dp.values()) if curr_dp else 0

    # 處理第2行及之後
    for row in range(2, n):
        next_dp = {}  # (mask_curr, mask_next) -> max_count

        for (mask_prev, mask_curr), count_prev in curr_dp.items():
            for mask_next in valid_masks:
                # 檢查mask_next的位置是否在平原上
                valid = True
                for col in range(m):
                    if (mask_next & (1 << col)) and grid[row][col] != "P":
                        valid = False
                        break
                if not valid:
                    continue

                # 檢查mask_curr和mask_next相容（距離=1）
                if not can_coexist(mask_curr, mask_next):
                    continue

                # 檢查mask_prev和mask_next（距離=2）
                # 距離為2，同列不能都有炮兵
                conflict = False
                for col in range(m):
                    if (mask_prev & (1 << col)) and (mask_next & (1 << col)):
                        conflict = True
                        break
                if conflict:
                    continue

                key = (mask_curr, mask_next)
                count_next = count_bits(mask_next)
                new_count = count_prev + count_next

                if key not in next_dp:
                    next_dp[key] = new_count
                else:
                    next_dp[key] = max(next_dp[key], new_count)

        curr_dp = next_dp

    # ===== 返回答案 =====
    return max(curr_dp.values()) if curr_dp else 0


def main():
    """讀取輸入並輸出結果。"""
    while True:
        try:
            line = input().strip()
            if not line:
                continue

            n, m = map(int, line.split())
            grid = []
            for _ in range(n):
                grid.append(input().strip())

            result = solve_artillery(n, m, grid)
            print(result)
        except EOFError:
            break


if __name__ == "__main__":
    main()
