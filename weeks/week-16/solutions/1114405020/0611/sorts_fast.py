def bubble_sort_fast(data: list) -> list:
    result = data[:]
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def quick_sort_fast(data: list) -> list:
    if len(data) < 2:
        return data[:]

    def median_of_three(a, b, c):
        return sorted([a, b, c])[1]

    pivot = median_of_three(data[0], data[len(data) // 2], data[-1])
    left = [x for x in data if x < pivot]
    middle = [x for x in data if x == pivot]
    right = [x for x in data if x > pivot]
    return quick_sort_fast(left) + middle + quick_sort_fast(right)

