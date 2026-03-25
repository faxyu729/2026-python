"""
UVA 10041 - 尋找最小距離總和

問題描述:
--------
黑社會老大 Vito Deadstone 要搬到紐約，親戚都住在 Lamafia 大道上。
需要找一間房子，使得到所有親戚房子的距離總和最小。

核心演算法原理:
--------------
統計學中的重要性質：使距離總和最小的位置是中位數（Median）
- 對於奇數個點，最優位置就是中位數
- 對於偶數個點，最優位置在兩個中間值之間的任何位置

時間複雜度: O(n log n) - 因為需要排序
空間複雜度: O(1) - 只使用常數額外空間
"""


def find_minimum_distance(relatives):
    """
    計算從最優位置到所有親戚房子的最小距離總和

    參數:
    ----
    relatives: list[int] 親戚房子的門牌號碼列表

    返回值:
    ------
    int 距離總和的最小值

    演算法步驟:
    ---------
    1. 對親戚的位置進行排序
    2. 找出中位數（中間值）
    3. 計算從中位數到所有親戚位置的距離總和
    4. 返回這個總和
    """

    # 步驟 1: 排序親戚的位置
    # 排序後我們可以更容易地找到中位數
    relatives.sort()

    # 步驟 2: 找出中位數位置
    # 中位數是排序後的中間值
    # 對於陣列長度為 n，中位數在索引 n//2 的位置
    # 例如: n=5 時，索引 5//2 = 2（第 3 個元素是中位數）
    median_index = len(relatives) // 2
    median = relatives[median_index]

    # 步驟 3: 計算距離總和
    # 使用迴圈遍歷所有親戚，計算每個親戚到中位數位置的距離
    total_distance = 0
    for relative_position in relatives:
        # 距離是位置差的絕對值
        distance = abs(relative_position - median)
        total_distance += distance

    # 步驟 4: 返回結果
    return total_distance


def read_and_process_input():
    """
    從標準輸入讀取測試資料並處理

    輸入格式:
    --------
    第一行: 測試資料組數 t
    對於每組測試資料:
        第一個整數: 親戚數量 r
        後續 r 個整數: 親戚的門牌號碼

    輸出:
    ----
    對每組測試資料，輸出距離總和的最小值
    """

    # 讀取測試資料組數
    t = int(input())

    # 處理每一組測試資料
    for _ in range(t):
        # 讀取一行包含親戚數量和他們的位置
        line = list(map(int, input().split()))

        # 第一個數字是親戚數量
        r = line[0]

        # 後續的數字是親戚的位置
        relatives = line[1 : r + 1]

        # 計算並輸出結果
        result = find_minimum_distance(relatives)
        print(result)


# 當直接運行此腳本時
if __name__ == "__main__":
    # 只運行輸入處理（用於線上評測）
    # 對於測試環境，直接調用 find_minimum_distance 函式
    pass
