def solve():
    t = int(input())

    for _ in range(t):
        m, n, q = map(int, input().split())
        grid = [input().strip() for _ in range(m)]
        print(m, n, q)

        for _ in range(q):
            r, c = map(int, input().split())
            center = grid[r][c]
            d = min(r, c, m - 1 - r, n - 1 - c)
            length = 1

            for size in range(1, d + 1):
                valid = True
                for i in range(r - size, r + size + 1):
                    for j in range(c - size, c + size + 1):
                        if grid[i][j] != center:
                            valid = False
                            break
                    if not valid:
                        break

                if valid:
                    length = 2 * size + 1
                else:
                    break

            print(length)

if __name__ == "__main__":
    solve()  