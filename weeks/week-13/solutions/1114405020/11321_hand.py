# -*- coding: utf-8 -*-
"""
UVA 11321 — 陷阱放置（手打程式）

題目：給定 N×M 的柏油路網格，起點在左側、終點在右側。
      茵可要放置 T 個陷阱，如果放置後仍有從左到右的路徑則可放。
"""

from collections import deque


def has_path(grid, N, M):
    """使用 BFS 檢查從左側到右側是否存在路徑"""
    q = deque()
    visited = [[False] * M for _ in range(N)]
    for i in range(N):
        if grid[i][0] == 0:
            q.append((i, 0))
            visited[i][0] = True

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while q:
        x, y = q.popleft()
        if y == M - 1:
            return True
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny] and grid[nx][ny] == 0:
                visited[nx][ny] = True
                q.append((nx, ny))

    return False


def process_traps(N, M, traps):
    """逐一檢查每個陷阱是否可以放置"""
    grid = [[0] * M for _ in range(N)]
    results = []

    for x, y in traps:
        grid[x][y] = 1
        if has_path(grid, N, M):
            results.append("<(_ _)>")
        else:
            results.append(">_<")
            grid[x][y] = 0

    return results


def solve_one_case(N, M, traps):
    """處理一組測試資料，回傳結果串列"""
    return process_traps(N, M, traps)


def main():
    """主程式：從標準輸入讀取資料並輸出結果"""
    import sys
    data = sys.stdin.read().strip().splitlines()
    if not data:
        return
    N, M, T = map(int, data[0].strip().split())
    traps = []
    for i in range(1, T + 1):
        x, y = map(int, data[i].strip().split())
        traps.append((x, y))
    results = process_traps(N, M, traps)
    print("\n".join(results))


if __name__ == "__main__":
    main()
