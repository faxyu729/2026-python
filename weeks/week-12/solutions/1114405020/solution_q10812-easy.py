"""
UVA 10812 - Beat the Spread! 簡易版本

這個版本使用更簡潔、更容易記憶的方式實現相同的功能。
代碼量少，邏輯清晰，適合快速開發和手寫面試。

核心公式（只需記住這個）：
  a = (S + D) / 2（較高分）
  b = (S - D) / 2（較低分）

驗證條件（只需記住這個）：
  1. (S + D) 是偶數
  2. (S - D) 是偶數
  3. b >= 0
"""


def solve():
    """
    簡易版：最小化代碼複雜度
    
    技巧：使用簡潔的條件判斷
    - 一行檢查所有條件
    - 直接計算和輸出結果
    """
    # 讀取測試組數
    n = int(input())
    
    for _ in range(n):
        # 讀入 S 和 D
        s, d = map(int, input().split())
        
        # 檢查所有驗證條件
        # 條件 1 和 2：(s+d) 和 (s-d) 都必須是偶數
        # 條件 3：(s-d) >= 0 即 s >= d
        if (s + d) % 2 == 0 and (s - d) % 2 == 0 and s >= d:
            # 計算並輸出
            a = (s + d) // 2
            b = (s - d) // 2
            print(a, b)
        else:
            print("impossible")


if __name__ == "__main__":
    solve()
