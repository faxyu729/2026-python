import math

def solve():
    import sys
    for line in sys.stdin:
        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break
        cnt = math.floor(math.sqrt(b)) - math.ceil(math.sqrt(a)) + 1
        print(cnt)

if __name__ == "__main__":
    solve()
