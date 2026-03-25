def solve(numbers):
    n = len(numbers)
    nums = sorted(numbers)

    if n % 2 == 1:
        
        a = nums[n // 2]
        r = 1
    else:
       
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
