import sys


def count_carries(a, b):
    """
    這是一個針對 CPE (UVA 10035 Primary Arithmetic) 簡單又容易記憶的版本 (-easy)。
    功能：計算兩個整數相加時，會產生幾次「進位」。
    """
    # 記錄總共進位的次數
    carry_count = 0
    # 記錄當下算出來是否要進位到下一位 (0 表示沒有，1 表示有)
    current_carry = 0

    # 只要這兩個數字任何一個還沒被除到變成 0，就繼續處理
    while a > 0 or b > 0:
        # 取得兩個數字最後面的那一位數 (例如 123 % 10 = 3)
        digit_a = a % 10
        digit_b = b % 10

        # 把這兩個位數相加，記得還要加上前一個位數進位過來的數字
        total = digit_a + digit_b + current_carry

        # 如果相加總和大於或等於 10，代表發生了進位
        if total >= 10:
            current_carry = 1
            carry_count += 1
        else:
            # 如果沒有超過 10，進位數字就歸零
            current_carry = 0

        # 把數字的最後一位砍掉，準備下一次迴圈處理十位、百位... (例如 123 // 10 = 12)
        a = a // 10
        b = b // 10

    return carry_count


def get_output_message(carries):
    """
    根據題目要求，根據進位次數回傳對應的字串
    注意單複數 (operation vs operations)
    """
    if carries == 0:
        return "No carry operation."
    elif carries == 1:
        return "1 carry operation."
    else:
        return f"{carries} carry operations."


def main():
    # 讀取所有的標準輸入並切分成一行一行
    input_text = sys.stdin.read().splitlines()

    for line in input_text:
        # 去除空白，跳過空行
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) >= 2:
            a = int(parts[0])
            b = int(parts[1])

            # 當遇到輸入都是 0 時，代表程式結束
            if a == 0 and b == 0:
                break

            # 計算進位次數
            carries = count_carries(a, b)
            # 轉換為題目要求的文字並印出
            print(get_output_message(carries))


if __name__ == "__main__":
    main()
