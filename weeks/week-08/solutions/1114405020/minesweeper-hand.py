case_num = 1

while True:
    line = input().split()
    n, m = int(line[0]), int(line[1])

    if n == 0 and m == 0:
        break

    grid = []
    for i in range(n):
        row = input().strip()
        grid.append(list(row))

    result = [row[:] for row in grid]

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == ".":
                count = 0
                for di, dj in directions:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < n and 0 <= nj < m:
                        if grid[ni][nj] == "*":
                            count += 1
                result[i][j] = str(count)

    print(f"Field #{case_num}:")
    for row in result:
        print("".join(row))
    print()

    case_num += 1
