# -*- coding: utf-8 -*-
"""
11349 對稱矩陣（Symmetric Matrix）—— 簡潔版

核心邏輯：雙層迴圈逐一檢查元素是否 ≥ 0 且與中心對稱位置相等。
比起完整版，此版本將所有程式碼寫在一個函數中，更容易記憶。
"""


def solve():
    """讀取標準輸入、判斷對稱矩陣、輸出結果"""
    import sys
    data = sys.stdin.read().splitlines()
    t = int(data[0])          # 測試組數
    out = []
    idx = 1

    for case in range(1, t + 1):
        # 讀取維度 N
        n = int(data[idx].split("=")[1])
        idx += 1

        # 用 list comprehension 一口氣讀完整個矩陣
        m = [list(map(int, data[idx + i].split())) for i in range(n)]
        idx += n

        # 檢查是否為中心對稱
        ok = True
        for i in range(n):
            for j in range(n):
                if m[i][j] < 0 or m[i][j] != m[n - 1 - i][n - 1 - j]:
                    ok = False
                    break
            if not ok:
                break

        out.append(f"Test #{case}: {'Symmetric.' if ok else 'Non-symmetric.'}")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
