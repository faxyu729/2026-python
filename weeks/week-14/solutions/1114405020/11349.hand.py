def solve():
    import sys
    data = sys.stdin.read().splitlines()
    t = int(data[0])
    out = []
    idx = 1

    for case in range(1, t + 1):
        n = int(data[idx].split("=")[1])
        idx += 1

        m = [list(map(int, data[idx + i].split())) for i in range(n)]
        idx += n

        ok = True
        for i in range(n):
            for j in range(n):
                if m[i][j] < 0 or m[i][j] != m[n - 1 - i][n - 1 - j]:
                    ok = False
                    break
            if not ok:
                break

        out.append(f"Test #{case}: {'Symmetric.' if ok else 'Non-symmetric.'}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
