def solve():
    n = int(input())
    
    for _ in range(n):
        s, d = map(int, input().split())
        
        if (s + d) % 2 == 0 and (s - d) % 2 == 0 and s >= d:
            a = (s + d) // 2
            b = (s - d) // 2
            print(a, b)
        else:
            print("impossible")

if __name__ == "__main__":
    solve()
