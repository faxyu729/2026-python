# -*- coding: utf-8 -*-
"""
UVA 11005 — Cheapest Base（簡易版本）

這是一版更容易記憶的寫法，核心概念只有三個步驟：
1. 將數字 n 轉成 base 進位的各位數字
2. 查表加總印刷成本
3. 找出成本最低的進位制（2 ~ 36）

解題口訣：「轉進位 → 算成本 → 找最省」
"""

def cheapest_bases(n, costs):
    """
    找出數字 n 在 2~36 進位制中，「印刷成本最低」的所有進位制。
    
    - n: 要查詢的十進位數字
    - costs: 長度為 36 的串列，依序對應字元 0~9, A~Z 的成本
    - 回傳: 成本最低的進位制串列（升序）
    """
    best_bases = []      # 儲存成本最低的進位制
    lowest_cost = None   # 當前最低成本
    
    # 逐一檢查 2 進位到 36 進位
    for base in range(2, 37):
        total = 0
        temp = n
        
        # === 步驟 1：把數字 n 轉成 base 進位 ===
        # 一直除以 base，取出每一位的餘數
        if temp == 0:
            digits = [0]            # 0 在任何進位都是 0
        else:
            digits = []
            while temp > 0:
                digits.append(temp % base)
                temp //= base
        
        # === 步驟 2：查表加總每一位的印刷成本 ===
        for d in digits:
            total += costs[d]
        
        # === 步驟 3：記錄最低成本的進位制 ===
        if lowest_cost is None or total < lowest_cost:
            lowest_cost = total
            best_bases = [base]      # 更省錢，取代之前的結果
        elif total == lowest_cost:
            best_bases.append(base)  # 一樣省錢，加入串列
    
    return best_bases


import unittest


class Test11005Easy(unittest.TestCase):
    """UVA 11005 簡易版測試"""

    def test_zero(self):
        """數字 0：任何進位都只是一個 '0'，全部一樣"""
        costs = [5] * 36
        self.assertEqual(cheapest_bases(0, costs), list(range(2, 37)))

    def test_fewest_digits(self):
        """成本相同，42 在 7~36 進位只需 2 位數，成本最低"""
        costs = [3] * 36
        # 42 在 base 2 需 6 位數，base 7~36 只需 2 位數
        self.assertEqual(cheapest_bases(42, costs), list(range(7, 37)))

    def test_base10_best(self):
        """0-9 成本=1，A-Z 成本=100 → 十進位對 15 最省"""
        costs = [1] * 10 + [100] * 26
        bases = cheapest_bases(15, costs)
        self.assertIn(10, bases)
        self.assertNotIn(16, bases)

    def test_hex_best(self):
        """A-F 成本=1，其他=100 → 十六進位對 255 最省"""
        costs = [100] * 10 + [1] * 6 + [100] * 20
        self.assertIn(16, cheapest_bases(255, costs))


if __name__ == "__main__":
    unittest.main()
