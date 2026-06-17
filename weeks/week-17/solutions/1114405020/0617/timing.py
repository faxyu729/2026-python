import time
import functools

def timeit(repeat=3):
    """
    A decorator that measures the execution time of a function.
    
    Args:
        repeat (int): Number of times to execute the function to calculate average.
    
    Raises:
        ValueError: If repeat is less than 1.
    """
    if repeat < 1:
        raise ValueError("repeat must be at least 1")

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            records = []
            for _ in range(repeat):
                start = time.perf_counter()
                result = f(*args, **kwargs)
                end = time.perf_counter()
                records.append(end - start)
            
            # Attach records and average to the wrapper function
            wrapper.records = records
            wrapper.last_elapsed = sum(records) / repeat
            
            return result
        
        # Initialize records and last_elapsed to avoid AttributeError before first call
        wrapper.records = []
        wrapper.last_elapsed = 0.0
        return wrapper
    
    return decorator
