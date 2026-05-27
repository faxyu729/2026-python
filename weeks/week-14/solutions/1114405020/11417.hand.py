import math

def solve():
    import sys
    for line in sys.stdin:
        n = int(line.strip())
        if n == 0:
            break
        total = 0
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                total += math.gcd(i, j)
        print(total)

if __name__ == "__main__":
    solve()
