"""
題目 10071 - 計算六元組個數問題（簡單易記版本）

====== 問題理解 ======
• 給定一個數字集合S，包含N個不重複的整數
• 計算有多少個六元組(a,b,c,d,e,f)滿足：a+b+c+d+e=f
• a、b、c、d、e、f都必須從S中選取（允許重複選擇）

====== 為什麼這個問題有趣？ ======
直觀地，我們可能想到：
  迴圈a: 迴圈b: 迴圈c: 迴圈d: 迴圈e: 迴圈f: 檢查a+b+c+d+e==f
但這需要O(N^6)時間，當N=100時，就是10^12次操作，太慢了！

改進方案：
  與其檢查每個f，不如先把所有a+b+c+d+e的和計算好，
  然後對於每個f，直接查詢有多少個和等於f。
  這樣就只需要O(N^5)時間！

====== 演算法核心思想 ======
1. 第一階段（預處理）：
   用5層迴圈計算所有(a,b,c,d,e)的和
   用字典記錄每個和出現多少次

2. 第二階段（計數）：
   遍歷每個f
   查字典：有多少個(a,b,c,d,e)的和等於f
   累加這些個數

====== 時間對比 ======
N=100的情況：
  • 暴力法：10^12次操作 → 可能需要幾小時
  • 優化法：(100^5 + 100) = 10^10次操作 → 幾秒鐘

====== 複雜度分析 ======
時間複雜度：O(N^5 + N) = O(N^5)
  • 計算所有五元組和：5層迴圈 = N^5次
  • 遍歷f計數：N次

空間複雜度：O(K)，K是不同和的個數
  • 最壞情況：K = N^5（每個和都不同）
  • 實際情況：K遠小於N^5
"""


def solve(input_string):
    """
    簡單易記的解法 - 使用預處理+字典查詢

    參數：
        input_string (str)：輸入字符串

    返回：
        int：六元組個數

    ====== 核心想法 ======
    分兩步走：
    1. 先計算好所有(a,b,c,d,e)的和
    2. 再查詢有多少個和等於每個f
    """
    # ====== 輸入解析 ======
    lines = input_string.strip().split("\n")
    n = int(lines[0])

    # 讀取集合S
    S = [int(lines[i]) for i in range(1, n + 1)]

    # ====== 步驟1：計算所有五元組之和及其出現次數 ======
    # sum_count[x] = 有多少個五元組(a,b,c,d,e)的和等於x
    sum_count = {}

    # 五層迴圈：枚舉所有(a,b,c,d,e)組合
    for a in S:
        for b in S:
            for c in S:
                for d in S:
                    for e in S:
                        # 計算這個五元組的和
                        total = a + b + c + d + e

                        # 記錄該和的出現次數
                        # sum_count.get(total, 0) 的意思是：
                        #   如果total在字典中，返回對應的值
                        #   否則返回0
                        sum_count[total] = sum_count.get(total, 0) + 1

    # ====== 步驟2：遍歷所有f，計算符合條件的六元組 ======
    # 對於每個f，如果存在(a,b,c,d,e)使得和等於f，
    # 則這些(a,b,c,d,e)的個數就是貢獻給該f的六元組個數
    result = 0
    for f in S:
        # 檢查：是否存在五元組和等於f？
        if f in sum_count:
            # 存在！有sum_count[f]個這樣的五元組
            result += sum_count[f]

    return result


# ====== 測試和驗證 ======
if __name__ == "__main__":
    tests = [
        # (輸入, 預期輸出, 描述)
        ("1\n0", 1, "單元素集合{0}"),
        ("2\n0\n1", 6, "兩元素集合{0,1}"),
        ("3\n-1\n0\n1", 141, "三元素集合{-1,0,1}"),
        ("3\n1\n2\n3", 0, "正數集合{1,2,3}無解"),
        ("3\n0\n1\n2", 21, "三元素集合{0,1,2}"),
        ("1\n5", 0, "單元素非零集合{5}無解"),
    ]

    print("====== Easy Version Test Results ======")
    all_pass = True
    for inp, expected, desc in tests:
        result = solve(inp)
        match = result == expected
        all_pass = all_pass and match
        status = "PASS" if match else "FAIL"
        print(f"{status}: {desc}")
        if not match:
            print(f"  Expected {expected}, Got {result}")

    print(f"\n====== Summary ======")
    print(f"{'All tests passed!' if all_pass else 'Some tests failed'}")
