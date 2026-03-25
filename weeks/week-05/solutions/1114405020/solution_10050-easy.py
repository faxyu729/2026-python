"""
UVA 10050 - 罷會損失天數（簡單版本）

核心邏輯很簡單:
1. 逐日檢查
2. 跳過週末（星期五和星期六）
3. 檢查是否有政黨罷會
4. 計數
"""


def hartal_loss(n, parties):
    """
    計算罷會損失天數

    參數:
    - n: 天數
    - parties: 政黨罷會參數列表
    """
    loss = 0

    # 逐天檢查
    for day in range(1, n + 1):
        # 計算星期幾（1=日, 2=一, ..., 6=五, 0=六）
        weekday = day % 7

        # 跳過週末（星期五6和星期六0）
        if weekday == 6 or weekday == 0:
            continue

        # 檢查是否有罷會
        if any(day % h == 0 for h in parties):
            loss += 1

    return loss


# 主程式
if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = int(input())
        parties = [int(input()) for _ in range(p)]
        print(hartal_loss(n, parties))
