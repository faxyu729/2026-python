def min_distance(relatives):
    relatives.sort()
    mid = relatives[len(relatives) // 2]
    return sum(abs(pos - mid) for pos in relatives)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        data = list(map(int, input().split()))
        r = data[0]
        relatives = data[1 : r + 1]
        print(min_distance(relatives))