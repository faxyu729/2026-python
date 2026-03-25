def calculate_win_probability(n, p, i):
    if p == 0:
        return 0.0
    if p == 1.0:
        return 1.0 if i == 1 else 0.0

    q = 1 - p
    return (p * q ** (i - 1)) / (1 - q**n)

if __name__ == "__main__":
    s = int(input())
    for _ in range(s):
        parts = input().split()
        n, p, i = int(parts[0]), float(parts[1]), int(parts[2])
        result = calculate_win_probability(n, p, i)
        print(f"{result:.4f}")
