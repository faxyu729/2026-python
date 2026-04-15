a = int(input())

if a == 1:
    print(5)
else:
    best_sum = float("inf")
    best_b = None
    best_c = None

    for c in range(a + 1, a * a + 1):
        numerator = a * c + 1
        denominator = c - a

        if numerator % denominator == 0:
            b = numerator // denominator

            if b > 0:
                current_sum = b + c
                if current_sum < best_sum:
                    best_sum = current_sum
                    best_b = b
                    best_c = c

    print(best_sum)
