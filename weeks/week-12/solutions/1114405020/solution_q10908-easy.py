"""
UVA 10908 - Largest Square 簡易版本

這個版本使用最簡潔的方式實現相同的功能。
代碼量少，邏輯清晰，易於手寫和記憶。

核心思想：
從邊長 1 開始，逐漸增加（每次 +2），檢查正方形內字元是否都相同。
"""


def solve():
    """簡易版主程式"""
    # 讀取測試組數
    t = int(input())
    
    for _ in range(t):
        # 讀入網格尺寸和查詢數
        m, n, q = map(int, input().split())
        
        # 讀入網格
        grid = [input().strip() for _ in range(m)]
        
        # 輸出網格資訊
        print(m, n, q)
        
        # 處理每個查詢
        for _ in range(q):
            r, c = map(int, input().split())
            
            # 獲取中心字元
            center = grid[r][c]
            
            # 計算最大可能邊長
            d = min(r, c, m - 1 - r, n - 1 - c)
            length = 1
            
            # 逐漸增加邊長
            for size in range(1, d + 1):
                # 檢查邊長 2*size+1 的正方形
                valid = True
                for i in range(r - size, r + size + 1):
                    for j in range(c - size, c + size + 1):
                        if grid[i][j] != center:
                            valid = False
                            break
                    if not valid:
                        break
                
                if valid:
                    length = 2 * size + 1
                else:
                    break
            
            print(length)


if __name__ == "__main__":
    solve()
