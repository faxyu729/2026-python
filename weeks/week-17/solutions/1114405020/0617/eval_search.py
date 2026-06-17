from timing import timeit
from search import linear_search, binary_search
import random

# Define functions with timeit decorator for measurement
@timeit(repeat=5)
def measured_linear(data, target):
    return linear_search(data, target)

@timeit(repeat=5)
def measured_binary(data, target, check_sorted=False):
    return binary_search(data, target, check_sorted=check_sorted)

def run_eval():
    n = 100000
    data = list(range(n))
    target = n - 1 # Worst case for linear search
    
    print(f"Measuring with n={n}, target={target}...")
    
    measured_linear(data, target)
    print(f"Linear Search records: {measured_linear.records}")
    print(f"Linear Search average: {measured_linear.last_elapsed:.6f}s")
    
    measured_binary(data, target, check_sorted=False)
    print(f"Binary Search records: {measured_binary.records}")
    print(f"Binary Search average: {measured_binary.last_elapsed:.6f}s")

if __name__ == "__main__":
    run_eval()
