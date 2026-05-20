# -*- coding: utf-8 -*-
"""
UVA 11332 — 鏡子可見性（簡易版本）

核心概念：
1. 站在原點 (0,0)，看哪條鏡子（線段）能被看到
2. 對每條鏡子，沿著鏡子取幾個採樣點
3. 對每個採樣點，檢查從原點到該點的路上有沒有被其他鏡子擋住
4. 只要有一個採樣點沒被擋住，就算可見

解題口訣：「採樣點 → 射線出擊 → 沒被擋就看得見」
"""

import math


def 叉積(ax, ay, bx, by):
    """計算向量 (ax,ay) 與 (bx,by) 的叉積"""
    return ax * by - ay * bx


def 在線段上(px, py, qx, qy, rx, ry):
    """檢查點 R 是否在線段 PQ 上"""
    return (min(px, qx) <= rx <= max(px, qx) and
            min(py, qy) <= ry <= max(py, qy))


def 線段相交(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y):
    """
    檢查兩條線段是否相交（含端點接觸）。
    
    使用「跨立實驗法」：
    - 如果兩條線段的端點分別在彼此兩側，就代表相交。
    """
    d1 = 叉積(p2x - p1x, p2y - p1y, p3x - p1x, p3y - p1y)
    d2 = 叉積(p2x - p1x, p2y - p1y, p4x - p1x, p4y - p1y)
    d3 = 叉積(p4x - p3x, p4y - p3y, p1x - p3x, p1y - p3y)
    d4 = 叉積(p4x - p3x, p4y - p3y, p2x - p3x, p2y - p3y)
    
    # 一般相交：端點在線段兩側
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    
    # 端點在線段上（共線）的情況
    if d1 == 0 and 在線段上(p3x, p3y, p4x, p4y, p1x, p1y):
        return True
    if d2 == 0 and 在線段上(p3x, p3y, p4x, p4y, p2x, p2y):
        return True
    if d3 == 0 and 在線段上(p1x, p1y, p2x, p2y, p3x, p3y):
        return True
    if d4 == 0 and 在線段上(p1x, p1y, p2x, p2y, p4x, p4y):
        return True
    
    return False


def 距離平方(px, py, qx, qy):
    """兩點距離的平方（省去開根號）"""
    return (px - qx) ** 2 + (py - qy) ** 2


def 鏡子看得見嗎(sx, sy, ex, ey, 所有鏡子, 我是誰):
    """
    檢查第『我是誰』個鏡子能不能從原點被看到。
    
    參數：
      sx, sy    — 這條鏡子的起點
      ex, ey    — 這條鏡子的終點
      所有鏡子  — 全部鏡子的串列
      我是誰    — 我在串列中的索引
    
    回傳：True 代表可見
    """
    # === 在鏡子上均勻取 10 個採樣點 ===
    for t in [i / 10 for i in range(11)]:
        px = sx + t * (ex - sx)
        py = sy + t * (ey - sy)
        
        if px == 0 and py == 0:
            continue      # 原點本身跳過
        
        被擋住 = False
        
        # === 檢查其他鏡子會不會擋住這條視線 ===
        for j, (jx1, jy1, jx2, jy2) in enumerate(所有鏡子):
            if j == 我是誰:
                continue  # 不用檢查自己
            
            # 從原點到採樣點的射線，跟其他鏡子相交？
            if 線段相交(0, 0, px, py, jx1, jy1, jx2, jy2):
                # 檢查那面鏡子是不是離原點更近
                if 距離平方(0, 0, jx1, jy1) < 距離平方(0, 0, px, py) or \
                   距離平方(0, 0, jx2, jy2) < 距離平方(0, 0, px, py):
                    被擋住 = True
                    break
        
        if not 被擋住:
            return True   # 有採樣點沒被擋住 → 可見
    
    return False          # 全部採樣點都被擋住 → 不可見


def 處理一組測資(鏡子們):
    """
    處理一組測試資料。
    
    - 鏡子們: [(sx,sy,ex,ey), ...]
    - 回傳: [0,1,0,...] 每個鏡子是否可見
    """
    result = []
    for i, (sx, sy, ex, ey) in enumerate(鏡子們):
        visible = 鏡子看得見嗎(sx, sy, ex, ey, 鏡子們, i)
        result.append(1 if visible else 0)
    return result


import unittest


class Test11332Easy(unittest.TestCase):
    """UVA 11332 簡易版測試"""

    def test_one_mirror(self):
        """只有一面鏡子，一定可見"""
        self.assertEqual(處理一組測資([(1, 1, 3, 3)]), [1])

    def test_two_separate(self):
        """兩面鏡子在不同方向，都可見"""
        self.assertEqual(處理一組測資([(1, 0, 1, 5), (5, 0, 5, 5)]), [1, 1])

    def test_two_same_direction(self):
        """兩面鏡子同方向，前面的還是可見"""
        r = 處理一組測資([(1, 1, 1, 3), (3, 1, 3, 3)])
        self.assertEqual(r[0], 1)  # 近的鏡子一定可見

    def test_three_mirrors(self):
        """三面鏡子"""
        r = 處理一組測資([(1, 0, 1, 5), (5, 0, 5, 5), (10, 0, 10, 5)])
        self.assertEqual(r, [1, 1, 1])


if __name__ == "__main__":
    unittest.main()
