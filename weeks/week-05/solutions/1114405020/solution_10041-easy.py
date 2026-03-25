"""
UVA 10041 - 簡易版本

這個版本用更簡潔、更直觀的方式實現同樣的演算法。
核心想法：最優位置就是中位數！

簡單記憶方法:
1. 排序列表
2. 取中位數
3. 計算總距離
"""


def min_distance(relatives):
    """
    簡單版本：找到最小距離總和

    邏輯很簡單：
    - 排序位置
    - 從中間拿出中位數
    - 計算所有距離
    """

    # 排序
    relatives.sort()

    # 取中位數（中間值）
    mid = relatives[len(relatives) // 2]

    # 計算距離總和：把所有位置的距離加起來
    return sum(abs(pos - mid) for pos in relatives)


# 簡單的交互式版本
if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        data = list(map(int, input().split()))
        r = data[0]
        relatives = data[1 : r + 1]
        print(min_distance(relatives))
