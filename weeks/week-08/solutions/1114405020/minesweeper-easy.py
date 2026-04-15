"""
踩地雷 (Minesweeper) - 簡單版本

簡化說明：
使用更直觀的方式實作踩地雷
"""


def solve_minesweeper_easy(grid):
    """
    踩地雷簡易版本

    基本思路：
    1. 複製輸入網格
    2. 對每個空白格子，計算周圍地雷數
    3. 返回結果

    周圍 8 個方向：
    [(-1,-1), (-1,0), (-1,1)]
    [(0,-1),          (0,1) ]
    [(1,-1),  (1,0),  (1,1) ]
    """
    # 複製網格
    result = [list(row) for row in grid]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # 遍歷每個格子
    for i in range(rows):
        for j in range(cols):
            # 如果是空白格子，計算周圍地雷
            if grid[i][j] == ".":
                count = 0
                # 檢查周圍 8 個格子
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        # 跳過自己
                        if di == 0 and dj == 0:
                            continue

                        # 新坐標
                        ni, nj = i + di, j + dj

                        # 檢查是否在範圍內且是地雷
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if grid[ni][nj] == "*":
                                count += 1

                # 填入地雷數量
                result[i][j] = str(count)

    return result


# 簡單測試
if __name__ == "__main__":
    # 測試案例 1
    grid1 = [
        ["*", ".", ".", "."],
        [".", ".", ".", "."],
        [".", "*", ".", "."],
        [".", ".", ".", "."],
    ]

    print("測試案例 1:")
    print("輸入:")
    for row in grid1:
        print("".join(row))

    result1 = solve_minesweeper_easy(grid1)
    print("\n輸出:")
    for row in result1:
        print("".join(row))

    # 測試案例 2
    grid2 = [
        ["*", "*", ".", ".", "."],
        [".", ".", ".", ".", "."],
        [".", "*", ".", ".", "."],
    ]

    print("\n\n測試案例 2:")
    print("輸入:")
    for row in grid2:
        print("".join(row))

    result2 = solve_minesweeper_easy(grid2)
    print("\n輸出:")
    for row in result2:
        print("".join(row))
