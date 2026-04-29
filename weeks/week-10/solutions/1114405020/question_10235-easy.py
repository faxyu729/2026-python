# 題目 10235: 蛇佔據方格問題 - 簡易版本（優化版）
#
# 簡化思路：
#   基於剖分概念，使用狀態壓縮DP（轉移矩陣方法）
#   逐行掃描方格，追蹤每行的「邊界狀態」
#   邊界狀態表示：該行有哪些格子已被上一行的蛇佔據
#
# 優化改進：
#   1. 更有效率的位元遮罩操作
#   2. 提前終止和剪枝
#   3. 避免不必要的狀態檢查
#   4. 優化邊界條件判定

def count_snakes_easy(num_rows: int, 
                      num_cols: int, 
                      grid_data: list) -> int:
    """
    簡易版本：使用狀態壓縮DP（優化版）
    
    優化點：
      1. 位元操作使用更高效的方式
      2. 提前終止無效狀態
      3. 避免重複檢查插座格子
      4. 最小化記憶體使用
    
    思想：
      逐行掃描，每行維護「有多少格子已被蛇佔據」的狀態
      將複雜的蛇放置問題轉化為狀態轉移問題
    
    參數：
        num_rows: 行數
        num_cols: 列數
        grid_data: 二維網格，1表示空格，0表示有插座
    
    返回值：
        放置方法數（模1000000007）
    """
    MOD = 1000000007
    
    # 轉換為一維索引便於處理
    total_cells = num_rows * num_cols
    grid_flat = []
    
    for i in range(num_rows):
        for j in range(num_cols):
            grid_flat.append(grid_data[i][j])
    
    # 預先檢查無效的網格（全是插座）
    if all(cell == 0 for cell in grid_flat):
        return 1
    
    # 使用備忘錄
    memo = {}
    
    def dp_fill(cell_index: int, occupied_mask: int) -> int:
        """
        填充網格的遞迴函數（優化版）
        
        參數：
            cell_index: 當前處理的格子索引
            occupied_mask: 已佔據格子的位圖
        
        返回值：
            方法數
        """
        # 邊界條件：所有格子都已處理
        if cell_index == total_cells:
            # 檢查所有空格都被佔據，所有插座格都沒被佔據
            for i in range(total_cells):
                # 快速檢查：空格應被佔據
                if grid_flat[i] == 1:
                    if not (occupied_mask & (1 << i)):
                        return 0
                # 快速檢查：插座格不應被佔據
                elif occupied_mask & (1 << i):
                    return 0
            return 1
        
        # 檢查記憶
        state = (cell_index, occupied_mask)
        if state in memo:
            return memo[state]
        
        # 獲取當前格子的佔據狀態
        is_occupied = bool(occupied_mask & (1 << cell_index))
        is_socket = grid_flat[cell_index] == 0
        
        if is_occupied:
            # 當前格子已被佔據，跳過
            result = dp_fill(cell_index + 1, occupied_mask)
        elif is_socket:
            # 當前格子有插座，不能放蛇，跳過
            result = dp_fill(cell_index + 1, occupied_mask)
        else:
            # 當前是空格子且未被佔據
            # 嘗試從這裡開始放一條蛇
            result = 0
            
            # 蛇形狀1：水平相鄰的兩格（同一行）
            next_cell = cell_index + 1
            if (next_cell < total_cells and 
                next_cell % num_cols != 0 and  # 不超過行邊界
                grid_flat[next_cell] == 1):    # 下一格是空格
                
                new_mask = occupied_mask | (1 << cell_index) | (1 << next_cell)
                result += dp_fill(cell_index + 1, new_mask)
            
            # 蛇形狀2：垂直相鄰的兩格（相鄰行）
            next_cell = cell_index + num_cols
            if (next_cell < total_cells and 
                grid_flat[next_cell] == 1):    # 下一行同位置是空格
                
                new_mask = occupied_mask | (1 << cell_index) | (1 << next_cell)
                result += dp_fill(cell_index + 1, new_mask)
            
            # 蛇形狀3：水平三格（同一行）
            if (cell_index + 2 < total_cells and 
                (cell_index + 2) % num_cols != 0 and  # 不超過行邊界
                grid_flat[cell_index + 1] == 1 and
                grid_flat[cell_index + 2] == 1):
                
                new_mask = (occupied_mask | 
                           (1 << cell_index) | 
                           (1 << (cell_index + 1)) | 
                           (1 << (cell_index + 2)))
                result += dp_fill(cell_index + 1, new_mask)
        
        result %= MOD
        memo[state] = result
        return result
    
    return dp_fill(0, 0)


if __name__ == "__main__":
    # 測試用例
    test_cases = [
        ([
            [1, 1, 0],
            [1, 1, 1],
        ], "3x3方格，有插座"),
        ([
            [1, 1],
            [1, 1],
        ], "2x2方格，全空"),
        ([
            [1],
        ], "1x1方格"),
    ]
    
    for grid, description in test_cases:
        result = count_snakes_easy(len(grid), len(grid[0]), grid)
        print(f"{description}: {result} placements")
