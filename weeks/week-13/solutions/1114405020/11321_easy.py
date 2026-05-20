# -*- coding: utf-8 -*-
"""
UVA 11321 — 陷阱放置（簡易版本）

核心概念：
1. 起點在左邊，終點在右邊
2. 每次嘗試放一個陷阱，看左邊能不能走到右邊
3. 可以放 → 保留陷阱，不可以放 → 撤掉

解題口訣：「放陷阱 → BFS 看能不能走通 → 決定留不留」
"""

from collections import deque


def 左邊能走到右邊嗎(grid, N, M):
    """
    用 BFS 從左側出發，看能不能走到右側。
    
    - grid: N×M 網格，0=空的，1=陷阱
    - 回傳: True 代表可以走通
    """
    # 從左側邊界開始探索
    待探索 = deque()
    走過 = [[False] * M for _ in range(N)]
    
    for i in range(N):
        if grid[i][0] == 0:
            待探索.append((i, 0))
            走過[i][0] = True
    
    # 四個移動方向
    方向 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while 待探索:
        x, y = 待探索.popleft()
        if y == M - 1:          # 到右邊了！
            return True
        for dx, dy in 方向:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < M and not 走過[nx][ny] and grid[nx][ny] == 0:
                走過[nx][ny] = True
                待探索.append((nx, ny))
    
    return False


def 處理陷阱(N, M, 陷阱們):
    """
    逐一檢查每個陷阱能不能放。
    
    參數：
      N, M    — 網格大小
      陷阱們  — [(x1,y1), (x2,y2), ...] 要放的陷阱位置
    
    回傳：["<(_ _)>" 或 ">_<", ...]
    """
    網格 = [[0] * M for _ in range(N)]   # 0=空的
    結果 = []
    
    for x, y in 陷阱們:
        網格[x][y] = 1                    # 先放看看
        
        if 左邊能走到右邊嗎(網格, N, M):
            結果.append("<(_ _)>")        # 可放，留著
        else:
            結果.append(">_<")            # 會擋路，撤掉
            網格[x][y] = 0               # 恢復原狀
    
    return 結果


import unittest


class Test11321Easy(unittest.TestCase):
    """UVA 11321 簡易版測試"""

    def test_basic_ok(self):
        """角落的陷阱不影響路徑"""
        r = 處理陷阱(3, 4, [(0, 0)])
        self.assertEqual(r, ["<(_ _)>"])

    def test_blocked(self):
        """單列網格，中間放陷阱會擋路"""
        r = 處理陷阱(1, 4, [(0, 2)])
        self.assertEqual(r, [">_<"])

    def test_sequential_block(self):
        """依序放置，第二個擋路"""
        r = 處理陷阱(2, 3, [(0, 1), (1, 1)])
        self.assertEqual(r, ["<(_ _)>", ">_<"])

    def test_detour(self):
        """有替代路徑，陷阱可放"""
        r = 處理陷阱(3, 3, [(0, 0), (2, 2)])
        self.assertEqual(r, ["<(_ _)>", "<(_ _)>"])


if __name__ == "__main__":
    unittest.main()
