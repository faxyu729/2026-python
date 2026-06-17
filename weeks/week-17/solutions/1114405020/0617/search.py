from timing import timeit

def linear_search(data: list, target) -> int:
    """
    Perform a linear search to find the target in the data list.
    
    Args:
        data (list): The list to search through.
        target: The element to search for.
        
    Returns:
        int: The index of the target if found, otherwise -1.
    """
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1

def binary_search(data: list, target, check_sorted=True) -> int:
    """
    Perform a binary search to find the target in a sorted data list.
    
    Args:
        data (list): A sorted list to search through.
        target: The element to search for.
        check_sorted (bool): Whether to verify if the list is sorted. Defaults to True.
        
    Returns:
        int: The index of the target if found, otherwise -1.
        
    Raises:
        ValueError: If check_sorted is True and the provided data list is not sorted.
    """
    if check_sorted:
        # Check if the data is sorted
        for i in range(len(data) - 1):
            if data[i] > data[i+1]:
                raise ValueError("binary_search requires a sorted list")
            
    low = 0
    high = len(data) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return -1
