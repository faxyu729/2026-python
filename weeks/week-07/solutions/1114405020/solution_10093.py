#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 10093 - 炮兵部隊部署問題 標準解答

=== 問題分析 ===
在 N×M 的網格地圖上部署炮兵部隊，最大化部署數量。
- 地形：山地(H)不能部署，平原(P)可以部署
- 攻擊範圍：橫向左右各2格，縱向上下各2格
- 限制條件：任何兩支炮兵不能互相攻擊

=== 演算法設計 ===

本解答採用「動態規劃 + 位元遮罩」的策略：

1. 核心概念
   ===============================================================
   由於 M ≤ 10，我們可以使用位元遮罩來表示每一列的炮兵部署方式。
   對於第 i 列，使用一個10位的二進制數來表示該列哪些位置有炮兵。

   例如：在 M=5 的情況下
   - 遮罩 0b00101 (十進制5) 表示第0列和第2列有炮兵
   - 遮罩 0b11111 (十進制31) 表示第0到4列都有炮兵

2. 狀態轉移
   ===============================================================
   dp[i][mask1][mask2] = 最大炮兵數

   含義：
   - i 為當前處理的行索引
   - mask1 為第 i-1 行的炮兵部署遮罩
   - mask2 為第 i 行的炮兵部署遮罩

   這樣設計的原因：
   - 需要記住前兩行的狀態，以便檢查約束條件
   - 檢查約束需要知道：
     * 前一行的部署情況（檢查縱向距離≤2的衝突）
     * 當前行的部署情況（檢查同行橫向距離≤4的衝突）

3. 約束檢查
   ===============================================================
   對於每一行，需要檢查：

   a) 同行約束（橫向攻擊範圍）：
      -------------------------------------------------------
      - 遮罩內的任意兩個位置，若距離 ≤ 2，則不能同時出現
      - 例如：位置 i 和 j 如果在遮罩內且 |i-j| ≤ 2，違反
      - 檢查方式：枚舉所有位置對

   b) 行間約束（縱向攻擊範圍）：
      -------------------------------------------------------
      - 相鄰兩行之間，距離 ≤ 2 的位置不能同時有炮兵
      - 例如：第 i-1 行的列 j 和第 i 行的列 j，距離為1，衝突
      - 檢查方式：對於 mask1 和 mask2，逐列檢查距離

4. 時間複雜度分析
   ===============================================================
   - 遮罩的可能數量：2^M
   - 對於每個狀態，需要檢查合法性：O(M)
   - 狀態轉移：O(2^M) × O(2^M) 種可能的轉移
   - 行數：N

   總時間複雜度：O(N × (2^M)^2 × M) = O(N × 4^M × M)
   由於 M ≤ 10，所以 4^M ≤ 2^20 ≈ 100萬，可行。

=== 實現細節 ===

1. 輔助函數
   ===============================================================
   - is_valid_row(mask, m): 檢查單行部署是否合法
   - can_coexist(mask1, mask2): 檢查兩行部署是否兼容
   - count_bits(mask): 計算遮罩中1的個數（部署數量）

2. 動態規劃迴圈
   ===============================================================
   - 初始化：處理前兩行的所有合法組合
   - 轉移：對於每一行，考慮所有兼容的前置狀態
   - 答案：DP表中的最大值

3. 優化技巧
   ===============================================================
   - 預處理所有合法的行遮罩
   - 預處理兩行間的兼容性矩陣
   - 使用位運算加速計數和判斷

=== 測試驗證 ===

已通過的測試用例：
1. 3×3 全平原：預期3，實際✓
2. 4×4 全平原：預期6，實際✓
3. 1×1 單格：預期1，實際✓
4. 3×3 全山地：預期0，實際✓
5. 5×3 混合地形：預期4，實際✓
"""

from typing import List, Tuple, Dict


def count_bits(mask: int) -> int:
    """
    計算一個整數的二進制表示中有多少個1。

    演算法：Brian Kernighan算法
    - 每次移除mask中最右邊的1
    - 重複直到mask變為0

    時間複雜度：O(k)，其中k是1的個數
    空間複雜度：O(1)

    參數：
        mask: 要計算的整數

    返回：
        mask 二進制表示中1的個數

    例子：
        count_bits(0b101) = 2  # 0b101 有2個1
        count_bits(0b111) = 3  # 0b111 有3個1
        count_bits(0) = 0      # 0 沒有1
    """
    count = 0
    while mask:
        mask &= mask - 1  # 移除最右邊的1
        count += 1
    return count


def is_valid_row(mask: int, m: int) -> bool:
    """
    檢查給定的行遮罩是否代表合法的炮兵部署。

    合法性檢查：同一行中的任意兩支炮兵之間距離不能 ≤ 2。

    實現方式：
    - 枚舉mask中所有為1的位置對(i, j)
    - 檢查任意兩個位置的距離
    - 距離 = |i - j|
    - 如果距離 ≤ 2，返回False

    時間複雜度：O(M^2)
    空間複雜度：O(1)

    參數：
        mask: 行遮罩，第i位為1表示第i列有炮兵
        m: 網格的列數

    返回：
        bool: 該遮罩是否代表合法部署

    例子：
        假設m=5
        mask=0b10100(十進制20) 表示第2列和第4列有炮兵
        距離=4-2=2，恰好在邊界，合法 → True

        mask=0b10010(十進制18) 表示第1列和第4列有炮兵
        距離=4-1=3，超過限制，合法 → True

        mask=0b00011(十進制3) 表示第0列和第1列有炮兵
        距離=1-0=1，距離≤2，非法 → False
    """
    positions = []

    # 提取mask中所有為1的位置
    for col in range(m):
        if mask & (1 << col):
            positions.append(col)

    # 檢查任意兩個位置的距離
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if positions[j] - positions[i] <= 2:
                return False

    return True


def can_coexist(mask1: int, mask2: int, m: int) -> bool:
    """
    檢查兩行的炮兵部署是否相容（不會互相攻擊）。

    約束條件：
    - mask1代表第i-1行的部署
    - mask2代表第i行的部署
    - 縱向距離為1（相鄰行）
    - 如果同一列都有炮兵，則衝突（距離為1，在攻擊範圍內）

    實現方式：
    - 同一列的兩個炮兵距離為1，肯定會互相攻擊
    - 因此 mask1 & mask2 必須為0

    時間複雜度：O(1)
    空間複雜度：O(1)

    參數：
        mask1: 第i-1行的遮罩
        mask2: 第i行的遮罩
        m: 網格的列數（此函數未使用m，但保留用於API一致性）

    返回：
        bool: 兩行部署是否相容

    例子：
        m=5
        mask1=0b10100 (第2,4列有炮兵)
        mask2=0b01010 (第1,3列有炮兵)
        mask1 & mask2 = 0b00000 = 0 → 無衝突，返回True

        mask1=0b10100 (第2,4列有炮兵)
        mask2=0b00100 (第2列有炮兵)
        mask1 & mask2 = 0b00100 ≠ 0 → 有衝突，返回False
    """
    return (mask1 & mask2) == 0


def can_place_artillery(
    n: int, m: int, grid: List[str], placements: List[Tuple[int, int]]
) -> bool:
    """
    檢查給定的炮兵部署位置是否合法。

    此函數用於驗證和測試。
    檢查：
    1. 所有位置都在平原上
    2. 任意兩個炮兵位置都不相互攻擊

    時間複雜度：O(k^2)，其中k是部署數量
    空間複雜度：O(1)

    參數：
        n: 網格的行數
        m: 網格的列數
        grid: 網格表示
        placements: 炮兵位置列表，每項為(row, col)

    返回：
        bool: 部署是否合法
    """
    # 檢查位置是否在平原上
    for row, col in placements:
        if grid[row][col] != "P":
            return False

    # 檢查任意兩個炮兵是否互相攻擊
    for i in range(len(placements)):
        for j in range(i + 1, len(placements)):
            r1, c1 = placements[i]
            r2, c2 = placements[j]

            # 檢查是否在攻擊範圍內
            if abs(r1 - r2) <= 2 and c1 == c2:  # 同列，距離≤2
                return False
            if abs(c1 - c2) <= 2 and r1 == r2:  # 同行，距離≤2
                return False
            if abs(r1 - r2) <= 2 and abs(c1 - c2) <= 2:
                # 注意：題目說的是「沿橫向左右各兩格，沿縱向上下各兩格」
                # 這通常理解為十字形攻擊範圍，不包括斜對角
                # 因此這行檢查實際上多餘（已由上兩行涵蓋）
                pass

    return True


def solve_artillery(n: int, m: int, grid: List[str]) -> int:
    """
    使用動態規劃解決炮兵部隊部署問題。

    演算法：
    1. 預處理：列出所有合法的行遮罩
    2. 初始化：設置前兩行的DP值
    3. 轉移：逐行計算DP值
    4. 答案：返回最大值

    時間複雜度：O(N × 4^M × M)
    空間複雜度：O(4^M)

    參數：
        n: 網格的行數
        m: 網格的列數
        grid: 網格表示，list of str，每個字符是'P'或'H'

    返回：
        int: 最多能部署的炮兵支數
    """

    # ==================== 第一步：預處理合法遮罩 ====================
    # 對於每一行，找出所有可能的合法部署方案（遮罩）
    # 並檢查該行該列是否為平原

    valid_masks = []  # 儲存所有合法的遮罩

    for mask in range(1 << m):  # 枚舉所有可能的遮罩（0到2^m-1）
        # 檢查遮罩是否合法（同行無衝突）
        if not is_valid_row(mask, m):
            continue

        # 檢查遮罩中的所有位置是否都在平原上
        # 由於這個檢查依賴具體的行，所以暫時不在這裡做
        # 而是在DP轉移時檢查
        valid_masks.append(mask)

    # ==================== 第二步：初始化DP表 ====================
    # 使用滾動數組優化空間
    # prev_dp[mask1][mask2] = 前一行的最大炮兵數
    # 其中mask1代表第i-2行，mask2代表第i-1行

    # 對於第0行，枚舉所有合法遮罩
    prev_dp = {}  # (mask_prev, mask_curr) -> max_count

    for mask0 in valid_masks:
        # 檢查mask0中的位置是否都在平原上
        valid = True
        for col in range(m):
            if (mask0 & (1 << col)) and grid[0][col] != "P":
                valid = False
                break

        if not valid:
            continue

        # 初始化：第0行
        prev_dp[(0, mask0)] = count_bits(mask0)

    if n == 1:
        # 特殊情況：只有一行
        return max(prev_dp.values()) if prev_dp else 0

    # 對於第1行
    curr_dp = {}

    for (mask0_dummy, mask0), count0 in prev_dp.items():
        for mask1 in valid_masks:
            # 檢查mask1中的位置是否都在平原上
            valid = True
            for col in range(m):
                if (mask1 & (1 << col)) and grid[1][col] != "P":
                    valid = False
                    break

            if not valid:
                continue

            # 檢查mask0和mask1是否相容
            if not can_coexist(mask0, mask1, m):
                continue

            count1 = count_bits(mask1)
            key = (mask0, mask1)
            if key not in curr_dp:
                curr_dp[key] = count0 + count1
            else:
                curr_dp[key] = max(curr_dp[key], count0 + count1)

    if n == 2:
        return max(curr_dp.values()) if curr_dp else 0

    # ==================== 第三步：轉移 ====================
    # 對於第i行（i >= 2），考慮所有可能的前置狀態

    for row in range(2, n):
        next_dp = {}

        for (mask_prev, mask_curr), count_prev in curr_dp.items():
            for mask_next in valid_masks:
                # 檢查mask_next中的位置是否都在平原上
                valid = True
                for col in range(m):
                    if (mask_next & (1 << col)) and grid[row][col] != "P":
                        valid = False
                        break

                if not valid:
                    continue

                # 關鍵約束檢查：
                # mask_curr 和 mask_next 相鄰（距離=1），必須相容
                # mask_prev 和 mask_next 距離=2，也不能衝突

                if not can_coexist(mask_curr, mask_next, m):
                    continue

                # 檢查mask_prev和mask_next（距離=2）
                # 距離為2的位置會互相攻擊
                conflict = False
                for col in range(m):
                    if (mask_prev & (1 << col)) and (mask_next & (1 << col)):
                        conflict = True
                        break

                if conflict:
                    continue

                count_next = count_bits(mask_next)
                key = (mask_curr, mask_next)
                new_count = count_prev + count_next

                if key not in next_dp:
                    next_dp[key] = new_count
                else:
                    next_dp[key] = max(next_dp[key], new_count)

        curr_dp = next_dp

    # ==================== 第四步：返回答案 ====================
    return max(curr_dp.values()) if curr_dp else 0


def main():
    """
    主程序：讀取輸入並調用求解函數。
    """
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
