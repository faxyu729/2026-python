import sys


def solve(a, b):
    # 手打版：計算進位並直接回傳結果字串
    carry = 0
    ans = 0

    while a > 0 or b > 0:
        if (a % 10) + (b % 10) + carry >= 10:
            carry = 1
            ans += 1
        else:
            carry = 0
        a //= 10
        b //= 10

    if ans == 0:
        return "No carry operation."
    elif ans == 1:
        return "1 carry operation."
    else:
        return f"{ans} carry operations."


def main():
    lines = sys.stdin.read().splitlines()
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2:
            a, b = int(parts[0]), int(parts[1])
            if a == 0 and b == 0:
                break
            print(solve(a, b))


if __name__ == "__main__":
    main()
