import sys
from collections import Counter


def solve(lines):
    """
    統計輸入字串中英文字母出現的頻率。
    大小寫視為相同，統一轉為大寫。
    排序規則：次數由大到小排序；若次數相同，則按字母順序（A-Z）由小到大排序。
    """
    # 將所有文字轉大寫，並過濾出英文字母
    all_text = "".join(lines).upper()
    letters = [char for char in all_text if char.isalpha()]

    # 計算每個字母的出現次數
    counter = Counter(letters)

    # 將結果轉換為列表並排序
    # x[0] 是字母，x[1] 是次數
    # 根據題意：先依次數(降序)排，再依字母(升序)排
    # 由於 Python 的 sort 預設是升序，所以我們可以用 -x[1] 讓次數變成降序
    sorted_items = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

    return sorted_items


def main():
    # 讀取標準輸入
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return

    try:
        n = int(input_data[0].strip())
    except ValueError:
        return

    # 取得後續的 n 列密文
    lines = input_data[1 : n + 1]

    # 取得解答
    ans = solve(lines)

    # 輸出結果
    for char, count in ans:
        print(f"{char} {count}")


if __name__ == "__main__":
    main()
