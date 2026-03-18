import sys


def solve(a, b):
    # 手打版：簡單使用 abs 回傳絕對值差
    return abs(a - b)


def main():
    # 讀取所有測資
    lines = sys.stdin.read().splitlines()
    for line in lines:
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) >= 2:
            a = int(parts[0])
            b = int(parts[1])
            print(solve(a, b))


if __name__ == "__main__":
    main()
