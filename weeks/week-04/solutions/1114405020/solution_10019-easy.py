import sys


def solve(a, b):
    """
    這是一個針對 CPE (UVA 10055/10019 Hashmat the Brave Warrior) 簡單又容易記憶的版本 (-easy)。
    功能：計算並回傳兩個整數的差的絕對值。
    """
    # 題目要求的是「Hashmat 與敵人士兵數目的差（正數）」
    # 也就是不管輸入順序為何，我們只要知道兩個數字相減後的「絕對值」即可。

    # 寫法一：使用內建的 abs() 函數 (最推薦，考試最不會忘記)
    # abs 意思是 absolute value (絕對值)
    return abs(a - b)

    # 寫法二：如果你忘記 abs，可以自己用 if 判斷誰大誰小
    # if a > b:
    #     return a - b
    # else:
    #     return b - a


def main():
    # 讀取標準輸入（所有行）
    # 因為測資可能有很多行，所以用 sys.stdin.read().splitlines() 取得每一行
    input_text = sys.stdin.read().splitlines()

    # 逐行處理
    for line in input_text:
        # 如果是空行就跳過
        if not line.strip():
            continue

        # 用空白把每一行的兩個數字切開
        parts = line.split()

        # 確保有兩個數字
        if len(parts) >= 2:
            a = int(parts[0])
            b = int(parts[1])

            # 呼叫簡易版的函式處理並印出
            print(solve(a, b))


if __name__ == "__main__":
    main()
