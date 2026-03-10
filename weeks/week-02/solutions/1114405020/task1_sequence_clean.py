def remove_duplicates_preserve_order(nums):
    seen = set()
    result = []
    for num in nums:
        if num not in seen:
            seen.add(num)
            result.append(num)
    return result

def get_even_numbers(nums):
    return [num for num in nums if num % 2 == 0]

def sequence_clean(input_str):
    if not input_str.strip():
        return {
            "dedupe": "",
            "asc": "",
            "desc": "",
            "evens": ""
        }
    
    nums = list(map(int, input_str.split()))
    
    dedupe_nums = remove_duplicates_preserve_order(nums)
    asc_nums = sorted(nums)
    desc_nums = sorted(nums, reverse=True)
    even_nums = get_even_numbers(nums)
    
    return {
        "dedupe": " ".join(map(str, dedupe_nums)),
        "asc": " ".join(map(str, asc_nums)),
        "desc": " ".join(map(str, desc_nums)),
        "evens": " ".join(map(str, even_nums))
    }
