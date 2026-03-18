import sys


def solve(n, k, weighings):
    # 手打的簡單版本，用於 CPE 考試記憶
    possible = []

    for i in range(1, n + 1):
        is_light = True
        is_heavy = True

        for count, left, right, res in weighings:
            in_left = i in left
            in_right = i in right

            if res == "=":
                if in_left or in_right:
                    is_light = False
                    is_heavy = False
            elif res == "<":
                if not in_left:
                    is_light = False
                if not in_right:
                    is_heavy = False
            elif res == ">":
                if not in_right:
                    is_light = False
                if not in_left:
                    is_heavy = False

        if is_light or is_heavy:
            possible.append(i)

    if len(possible) == 1:
        return possible[0]
    return 0


def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    m = int(input_data[0])
    idx = 1

    for case_num in range(m):
        n = int(input_data[idx])
        k = int(input_data[idx + 1])
        idx += 2

        weighings = []
        for _ in range(k):
            count = int(input_data[idx])
            idx += 1

            left = [int(input_data[i]) for i in range(idx, idx + count)]
            idx += count

            right = [int(input_data[i]) for i in range(idx, idx + count)]
            idx += count

            res = input_data[idx]
            idx += 1

            weighings.append((count, left, right, res))

        print(solve(n, k, weighings))
        if case_num < m - 1:
            print()


if __name__ == "__main__":
    main()
