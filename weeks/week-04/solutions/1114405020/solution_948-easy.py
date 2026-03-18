import sys


def solve(n, k, weighings):
    """
    用更簡單、更容易記憶的方式寫出找出假幣的程式 (-easy)。

    n: 硬幣的數量
    k: 秤重次數
    weighings: 秤重紀錄的列表
    """
    possible_fakes = []

    # 逐一檢查每一枚硬幣，看看它是否可能是「假幣」
    for coin_id in range(1, n + 1):
        # 先假設這枚硬幣是「較輕」的假幣
        is_lighter_fake = True

        # 同時假設這枚硬幣是「較重」的假幣
        is_heavier_fake = True

        # 檢查所有的秤重紀錄
        for count, left_side, right_side, result in weighings:
            # 硬幣有沒有在左邊盤子？
            in_left = coin_id in left_side
            # 硬幣有沒有在右邊盤子？
            in_right = coin_id in right_side

            # 如果天平平衡 (=)，假幣絕對不可能在天平上
            if result == "=":
                if in_left or in_right:
                    # 既然在天平上，它就不是假幣
                    is_lighter_fake = False
                    is_heavier_fake = False

            # 如果左邊比較輕 (<)，那「較輕的假幣」必須在左邊，「較重的假幣」必須在右邊
            elif result == "<":
                if not in_left:
                    # 如果沒在左邊，就不可能是較輕的假幣
                    is_lighter_fake = False
                if not in_right:
                    # 如果沒在右邊，就不可能是較重的假幣
                    is_heavier_fake = False

            # 如果左邊比較重 (>)，那「較輕的假幣」必須在右邊，「較重的假幣」必須在左邊
            elif result == ">":
                if not in_right:
                    # 如果沒在右邊，就不可能是較輕的假幣
                    is_lighter_fake = False
                if not in_left:
                    # 如果沒在左邊，就不可能是較重的假幣
                    is_heavier_fake = False

        # 檢查完所有紀錄後，如果這枚硬幣有可能是假幣 (不論輕重)，就記下來
        if is_lighter_fake or is_heavier_fake:
            possible_fakes.append(coin_id)

    # 如果只有唯一的一枚硬幣有可能是假幣，那就是它了！
    if len(possible_fakes) == 1:
        return possible_fakes[0]
    else:
        # 如果找不出唯一的假幣，或是無法確定，就回傳 0
        return 0


def main():
    # 讀取標準輸入的所有資料
    input_text = sys.stdin.read().split()
    if not input_text:
        return

    m = int(input_text[0])
    idx = 1

    # 處理每一組測試資料
    for case_num in range(m):
        n = int(input_text[idx])
        k = int(input_text[idx + 1])
        idx += 2

        weighings = []
        for _ in range(k):
            # 每邊放的數量
            count = int(input_text[idx])
            idx += 1

            # 左邊盤子的硬幣
            left_side = []
            for _ in range(count):
                left_side.append(int(input_text[idx]))
                idx += 1

            # 右邊盤子的硬幣
            right_side = []
            for _ in range(count):
                right_side.append(int(input_text[idx]))
                idx += 1

            # 秤重結果 (<, >, =)
            result = input_text[idx]
            idx += 1

            weighings.append((count, left_side, right_side, result))

        # 呼叫 solve 找出假幣並印出
        ans = solve(n, k, weighings)
        print(ans)

        # 測試資料間印出空白行
        if case_num < m - 1:
            print()


if __name__ == "__main__":
    main()
