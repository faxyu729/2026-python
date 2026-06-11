def timeit(func):
    def wrapper(*args, **kwargs):
        print("stub")
        return func(*args, **kwargs)
    return wrapper
