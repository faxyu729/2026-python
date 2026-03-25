def hartal_loss(n, parties):
    loss = 0
    for day in range(1, n + 1):
        weekday = day % 7
        if weekday == 6 or weekday == 0:
            continue
        if any(day % h == 0 for h in parties):
            loss += 1
    return loss

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = int(input())
        parties = [int(input()) for _ in range(p)]
        print(hartal_loss(n, parties))
