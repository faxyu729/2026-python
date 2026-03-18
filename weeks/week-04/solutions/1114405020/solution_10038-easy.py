import sys


def is_jolly(numbers):
    """
    這是一個針對 CPE (UVA 10038 Jolly Jumpers) 簡單又容易記憶的版本 (-easy)。
    功能：判斷一個整數序列相鄰兩數的絕對差，是否剛好涵蓋 1 到 n-1。
    """
    # 陣列的第一個數字是 n (序列的長度)
    n = numbers[0]

    # 陣列從第二個數字開始，才是真正的序列
    seq = numbers[1:]

    # 如果序列只有 1 個數字，沒有相鄰的數字可以相減，
    # 根據題意，它依然被視為 Jolly jumper
    if n == 1:
        return "Jolly"

    # 準備一個列表來收集所有相鄰數字的「絕對差」
    diffs = []

    # 用迴圈計算相鄰兩個數字的差 (總共會有 n-1 個差值)
    for i in range(n - 1):
        # abs() 用來計算絕對值
        diff = abs(seq[i] - seq[i + 1])
        diffs.append(diff)

    # 將算出來的差值由小到大排序
    diffs.sort()

    # 產生一個我們期望的列表：[1, 2, 3, ..., n-1]
    # range(1, n) 會產生 1 到 n-1 的數字
    expected = list(range(1, n))

    # 如果我們算出來的差值列表，跟我們期望的列表一模一樣
    if diffs == expected:
        return "Jolly"
    else:
        return "Not jolly"


def main():
    # 讀取所有的標準輸入並切分成一行一行
    input_text = sys.stdin.read().splitlines()

    for line in input_text:
        # 去除兩側空白，跳過空行
        line = line.strip()
        if not line:
            continue

        # 將字串切開並轉換為整數列表
        parts = line.split()
        numbers = [int(x) for x in parts]

        # 如果這一行有資料才處理
        if len(numbers) > 0:
            # 呼叫簡易版的函式處理並印出結果
            print(is_jolly(numbers))


if __name__ == "__main__":
    main()
