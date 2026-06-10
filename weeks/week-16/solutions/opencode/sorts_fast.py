_INSERTION_THRESHOLD = 16


def bubble_sort_fast(data: list) -> list:
    """Bubble sort 提前停止:一輪沒交換就直接結束"""
    result = data.copy()
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
    """Quick sort + median-of-three + 小區間切 insertion sort"""
    if len(data) <= 1:
        return data.copy()
    return _quick_sort(data, 0, len(data))


def _quick_sort(data: list, lo: int, hi: int) -> list:
    """回傳 data[lo:hi] 排序後的新 list"""
    n = hi - lo
    if n <= 1:
        return data[lo:hi]
    if n <= _INSERTION_THRESHOLD:
        return _insertion_sort(data[lo:hi])
    pivot = _median_of_three(data, lo, hi)
    left = [x for x in data[lo:hi] if x < pivot]
    middle = [x for x in data[lo:hi] if x == pivot]
    right = [x for x in data[lo:hi] if x > pivot]
    return _quick_sort(left, 0, len(left)) + middle + _quick_sort(right, 0, len(right))


def _median_of_three(data: list, lo: int, hi: int):
    """從 data[lo:hi] 取頭、中、尾三個值的中位數當 pivot"""
    mid = (lo + hi - 1) // 2
    a, b, c = data[lo], data[mid], data[hi - 1]
    if a > b:
        a, b = b, a
    if a > c:
        a, c = c, a
    if b > c:
        b, c = c, b
    return b


def _insertion_sort(data: list) -> list:
    result = data.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result
