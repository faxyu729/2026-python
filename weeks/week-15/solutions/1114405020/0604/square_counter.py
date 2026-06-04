def count_squares(a: int, b: int) -> int:
    if a > b:
        raise ValueError("a must be <= b")

    import math
    low = max(a, 0)
    start = math.ceil(math.sqrt(low))
    end = math.floor(math.sqrt(b))
    return max(0, end - start + 1)
