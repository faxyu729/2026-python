"""
UVA 10057 - 找尋最優密碼 (簡單版本)

簡潔設計: 最少行數，最易記憶
核心: 排序後找中位數
"""


def solve(numbers):
    """
    最簡單的解決方案
    """
    n = len(numbers)
    nums = sorted(numbers)

    if n % 2 == 1:
        # 奇數: 中位數
        a = nums[n // 2]
        r = 1
    else:
        # 偶數: 上中位數和下中位數之間
        a = nums[n // 2]
        r = nums[n // 2] - nums[n // 2 - 1] + 1

    return a, numbers.count(a), r


while True:
    n = int(input())
    if n == 0:
        break
    numbers = list(map(int, input().split()))
    a, c, r = solve(numbers)
    print(f"{a} {c} {r}")
