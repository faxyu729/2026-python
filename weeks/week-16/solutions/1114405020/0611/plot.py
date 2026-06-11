import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_results(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def plot_results(results: dict, out_path: str) -> None:
    plt.figure(figsize=(10, 6))
    sizes = sorted(next(iter(results.values())).keys(), key=int)
    for name, times in results.items():
        values = [times[s] for s in sizes]
        plt.plot(sizes, values, marker="o", label=name)

    plt.xlabel("Data Size (n)")
    plt.ylabel("Average Time (s)")
    plt.yscale("log")
    plt.title("Sorting Algorithm Performance Comparison")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
