import json
import random
from timing import timeit
from sorts import bubble_sort, quick_sort, merge_sort
from sorts_fast import bubble_sort_fast, quick_sort_fast


def make_data(n: int, seed: int = 42) -> list:
    random.seed(seed)
    return [random.randint(0, 10000) for _ in range(n)]


def run_benchmark(sizes=(500, 1000, 2000, 4000), repeats=3) -> dict:
    sorts = {
        "bubble_sort": bubble_sort,
        "quick_sort": quick_sort,
        "merge_sort": merge_sort,
        "bubble_sort_fast": bubble_sort_fast,
        "quick_sort_fast": quick_sort_fast,
        "builtin_sorted": sorted,
    }

    results = {}
    for name, func in sorts.items():
        func = timeit(func)
        results[name] = {}
        for n in sizes:
            times = []
            for _ in range(repeats):
                data = make_data(n)
                func(data)
                times.append(func.last_elapsed)
            avg = sum(times) / len(times)
            results[name][str(n)] = round(avg, 6)

    return results


def print_table(results):
    header = "Algorithm".ljust(16)
    sizes = sorted(next(iter(results.values())).keys(), key=int)
    for s in sizes:
        header += f"n={s}".rjust(14)
    print(header)
    print("-" * (16 + 14 * len(sizes)))
    for name, times in results.items():
        row = name.ljust(16)
        for s in sizes:
            row += f"{times[s]:>10.6f}s  "
        print(row)


if __name__ == "__main__":
    results = run_benchmark()
    print("\nBenchmark Results:\n")
    print_table(results)
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nresults.json saved.")
