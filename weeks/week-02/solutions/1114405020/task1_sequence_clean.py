def remove_duplicates_preserve_order(nums):
    """
    移除串列中的重複元素，並保留原本的出現順序。

    Args:
        nums (list): 包含整數的串列。

    Returns:
        list: 去除重複元素後的串列。
    """
    seen = set()
    result = []
    for num in nums:
        if num not in seen:
            seen.add(num)
            result.append(num)
    return result


def get_even_numbers(nums):
    """
    從串列中篩選出所有的偶數。

    Args:
        nums (list): 包含整數的串列。

    Returns:
        list: 僅包含偶數的串列。
    """
    return [num for num in nums if num % 2 == 0]


def sequence_clean(input_str):
    """
    處理數字字串，包含去重（保序）、升冪排序、降冪排序及提取偶數。

    Args:
        input_str (str): 以空白分隔的數字字串。

    Returns:
        dict: 包含 'dedupe', 'asc', 'desc', 'evens' 四個鍵的字典，值為處理後的空白分隔字串。
    """
    if not input_str.strip():
        return {"dedupe": "", "asc": "", "desc": "", "evens": ""}

    nums = list(map(int, input_str.split()))

    dedupe_nums = remove_duplicates_preserve_order(nums)
    asc_nums = sorted(nums)
    desc_nums = sorted(nums, reverse=True)
    even_nums = get_even_numbers(nums)

    return {
        "dedupe": " ".join(map(str, dedupe_nums)),
        "asc": " ".join(map(str, asc_nums)),
        "desc": " ".join(map(str, desc_nums)),
        "evens": " ".join(map(str, even_nums)),
    }
