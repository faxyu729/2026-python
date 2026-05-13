"""
UVA 10908 - Largest Square 完整解決方案

題目：
給定一個 M 行 N 列的字元網格，以及 Q 個查詢。
對於每個查詢，給定一個中心點座標 (r, c)，找出以該點為中心，
所有字元相同的最大正方形的邊長。

輸入說明：
- 第一行為測試組數 T
- 每組測試資料：
  - 第一行：M、N、Q（網格行數、列數、查詢數）
  - 接下來 M 行：網格的每一行（N 個字元）
  - 接下來 Q 行：每行兩個整數 r、c（查詢座標）

輸出說明：
- 對每組測試資料，先輸出一行 M N Q
- 接下來 Q 行：每行輸出對應查詢的最大正方形邊長
"""


def solve_q10908():
    """
    解題主程式
    
    核心邏輯：
    1. 對每組測試資料讀取網格和查詢
    2. 對於每個查詢點 (r, c)：
       - 獲取中心點的字元
       - 從邊長 1 開始逐漸增加（每次增加 2）
       - 檢查該邊長的正方形內所有字元是否相同
       - 當發現不符合時停止
    3. 輸出結果
    
    時間複雜度：
    - 對於單個查詢：O(邊長² ) ≈ O(min(M,N)²)
    - 對於 Q 個查詢：O(Q × min(M,N)²)
    
    空間複雜度：O(M × N)（存儲網格）
    """
    
    # 讀取測試組數
    t = int(input())
    
    # 逐組處理測試資料
    for _ in range(t):
        # 讀取網格尺寸和查詢數
        m, n, q = map(int, input().split())
        
        # 讀取 M 行網格
        grid = []
        for i in range(m):
            # 每一行是一個字串，包含 N 個字元
            grid.append(input().strip())
        
        # 輸出網格資訊
        print(f"{m} {n} {q}")
        
        # 處理 Q 個查詢
        for _ in range(q):
            # 讀取查詢點座標
            r, c = map(int, input().split())
            
            # 調用函式找出最大正方形邊長
            max_length = find_max_square(grid, r, c, m, n)
            
            # 輸出結果
            print(max_length)


def find_max_square(grid, r, c, m, n):
    """
    在網格中找出以 (r, c) 為中心的最大同字元正方形的邊長。
    
    參數：
        grid: 字元網格（列表的列表）
        r: 查詢點的行號
        c: 查詢點的列號
        m: 網格行數
        n: 網格列數
    
    返回：
        最大正方形的邊長（奇數）
    
    算法步驟：
    1. 獲取中心點的字元
    2. 計算最大可能的邊長（受邊界限制）
    3. 從邊長 1 開始，逐漸增加
    4. 對於每個邊長，檢查正方形內的所有字元
    5. 若都相同，記錄此邊長；若有不同，停止並返回前一個邊長
    """
    
    # 獲取中心點的字元
    center_char = grid[r][c]
    
    # 初始化最大邊長為 1
    max_length = 1
    
    # 計算最大可能的邊長
    # distance 是從中心到邊界的距離（向四個方向）
    # max_distance 是可以向外擴展的最大距離
    max_distance = min(r, c, m - 1 - r, n - 1 - c)
    
    # 最大可能的邊長
    # 例：distance = 2 時，邊長 = 2*2 + 1 = 5
    max_possible = 2 * max_distance + 1
    
    # 嘗試所有可能的邊長（1, 3, 5, 7, ...）
    # 正方形邊長必須為奇數，因為需要一個中心點
    for length in range(1, max_possible + 1, 2):
        
        # 計算距離中心的距離
        # 例：length = 1 時，distance = 0（只有中心點）
        #    length = 3 時，distance = 1（向各方向各 1 格）
        #    length = 5 時，distance = 2（向各方向各 2 格）
        distance = length // 2
        
        # 標記此邊長的正方形是否符合條件
        valid = True
        
        # 檢查以 (r, c) 為中心、邊長為 length 的正方形
        # 檢查範圍：[r-distance, r+distance] × [c-distance, c+distance]
        for i in range(r - distance, r + distance + 1):
            for j in range(c - distance, c + distance + 1):
                
                # 檢查是否超出邊界
                if i < 0 or i >= m or j < 0 or j >= n:
                    valid = False
                    break
                
                # 檢查字元是否與中心相同
                if grid[i][j] != center_char:
                    valid = False
                    break
            
            # 如果已經發現不符合，提前退出內層迴圈
            if not valid:
                break
        
        # 檢查結果
        if valid:
            # 符合條件，記錄此邊長
            max_length = length
        else:
            # 不符合條件，提前退出外層迴圈
            # 因為更大的邊長也不會符合
            break
    
    return max_length


if __name__ == "__main__":
    solve_q10908()
