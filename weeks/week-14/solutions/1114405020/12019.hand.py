D = {1:10, 2:21, 3:7, 4:4, 5:9, 6:6, 7:11, 8:8, 9:5, 10:10, 11:7, 12:12}
W = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def solve():
    import sys
    data = sys.stdin.read().splitlines()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        m, d = map(int, data[i].split())
        out.append(W[(2 + d - D[m]) % 7])
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
