"""
UVA 10050 - 計算因罷會損失的工作天數

問題描述:
--------
計算在N天內，因為多個政黨的罷會造成多少天的工作損失。
規則：
- 起始日是星期天
- 星期五(第6天)和星期六(第7天)不計算罷會
- 每個政黨每 h 天罷會一次

核心演算法:
---------
對於每一天，檢查：
1. 是否是星期五或星期六（跳過）
2. 是否有政黨罷會（檢查所有政黨）
3. 計算總損失天數
"""


def calculate_hartal_days(n, hartal_params):
    """
    計算N天內因罷會損失多少工作天

    參數:
    ----
    n: int 模擬天數
    hartal_params: list[int] 各政黨的罷會參數

    返回值:
    ------
    int 損失的工作天數

    演算法步驟:
    ---------
    1. 初始化損失天數為0
    2. 逐天檢查（第1天到第N天）
    3. 對每一天：
       a. 計算該天是星期幾（天數 % 7）
       b. 如果是星期五(6)或星期六(0，第7天)，跳過
       c. 檢查是否有政黨罷會（檢查天數是否是該政黨h的倍數）
       d. 如果有罷會，增加損失計數
    4. 返回總損失天數
    """

    # 初始化損失計數
    loss_days = 0

    # 逐天檢查（從第1天到第N天）
    for day in range(1, n + 1):
        # 計算該天是星期幾
        # day % 7 給出：
        # 1 = 星期日, 2 = 星期一, ..., 5 = 星期四, 6 = 星期五, 0 = 星期六
        day_of_week = day % 7

        # 如果是星期五(6)或星期六(0)，這天不計算罷會，跳過
        if day_of_week == 6 or day_of_week == 0:
            continue

        # 檢查是否有政黨罷會
        # 遍歷所有政黨的罷會參數
        has_hartal = False
        for h in hartal_params:
            # 如果該天是罷會參數的倍數，則該政黨罷會
            if day % h == 0:
                has_hartal = True
                break

        # 如果有罷會，計入損失
        if has_hartal:
            loss_days += 1

    return loss_days


def read_and_process_input():
    """
    從標準輸入讀取測試資料並處理

    輸入格式:
    --------
    第一行: T 測試資料組數
    對於每組測試資料:
        第一行: N 模擬天數
        第二行: P 政黨數量
        接下來P行: 每行一個整數 h，代表該政黨的罷會參數

    輸出:
    ----
    對每組測試資料，輸出損失的工作天數
    """

    # 讀取測試資料組數
    t = int(input())

    # 處理每一組測試資料
    for _ in range(t):
        # 讀取模擬天數
        n = int(input())

        # 讀取政黨數量
        p = int(input())

        # 讀取每個政黨的罷會參數
        hartal_params = []
        for _ in range(p):
            h = int(input())
            hartal_params.append(h)

        # 計算損失天數並輸出
        result = calculate_hartal_days(n, hartal_params)
        print(result)


# 當直接運行此腳本時
if __name__ == "__main__":
    # 取消註解下一行來運行輸入處理
    # read_and_process_input()
    pass
