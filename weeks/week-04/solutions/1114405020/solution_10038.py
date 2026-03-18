import sys


def solve(nums):
    # 手打版：運用 set 來快速比較 1 到 n-1 的差值是否齊全
    if not nums:
        return ""
    n = nums[0]
    seq = nums[1:]

    if n == 1:
        return "Jolly"

    # 計算相鄰元素的絕對差，並放入集合 (set) 自動去除重複
    diffs = set(abs(seq[i] - seq[i + 1]) for i in range(n - 1))

    # 若該集合剛好等於 {1, 2, ..., n-1}，就是 Jolly
    if diffs == set(range(1, n)):
        return "Jolly"
    else:
        return "Not jolly"


def main():
    lines = sys.stdin.read().splitlines()
    for line in lines:
        if not line.strip():
            continue
        nums = list(map(int, line.split()))
        if nums:
            print(solve(nums))


if __name__ == "__main__":
    main()
