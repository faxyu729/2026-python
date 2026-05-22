import csv
import platform
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent.parent.parent / "assets" / "stu-data"
OUTPUT_DIR = HERE / "output"

YEARS = [112, 113, 114]

_CJK_FONTS = {
    "Darwin":  ["Heiti TC", "Arial Unicode MS", "PingFang TC"],
    "Windows": ["Microsoft JhengHei", "Microsoft YaHei"],
    "Linux":   ["Noto Sans CJK TC", "WenQuanYi Zen Hei"],
}.get(platform.system(), ["sans-serif"])


def _apply_cjk_font():
    plt.rcParams["font.sans-serif"] = _CJK_FONTS + plt.rcParams["font.sans-serif"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False


def load_year(year: int, data_dir: Path = DATA_DIR) -> dict[str, int]:
    path = data_dir / f"{year}年新生資料庫.csv"
    result: dict[str, int] = {}
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dept = row["系所名稱"].strip()
            result[dept] = result.get(dept, 0) + 1
    return result


def get_top_depts(year_data: dict[int, dict], top_n: int = 8) -> list[str]:
    candidate: set[str] = set()
    for year, dept_counts in year_data.items():
        sorted_depts = sorted(dept_counts.items(), key=lambda x: -x[1])
        for dept, _ in sorted_depts[:top_n]:
            candidate.add(dept)
    totals: dict[str, int] = {}
    for dept_counts in year_data.values():
        for dept, count in dept_counts.items():
            totals[dept] = totals.get(dept, 0) + count
    sorted_candidates = sorted(
        (d for d in candidate if d in totals), key=lambda x: -totals[x]
    )
    return sorted_candidates[:top_n]


def plot_grouped_bar(year_data: dict[int, dict], top_depts: list[str]):
    _apply_cjk_font()

    dept_values = {dept: [] for dept in top_depts}
    for dept in top_depts:
        for year in YEARS:
            dept_values[dept].append(year_data[year].get(dept, 0))

    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(top_depts))
    n_years = len(YEARS)
    bar_width = 0.25

    colors = ["#4ECDC4", "#FFA07A", "#98D8C8"]
    for i, year in enumerate(YEARS):
        values = [dept_values[dept][i] for dept in top_depts]
        bars = ax.barh(x + i * bar_width, values, bar_width, label=f"{year} 學年", color=colors[i])
        for bar, v in zip(bars, values):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    str(v), va="center", fontsize=9)

    ax.set_yticks(x + bar_width * (n_years - 1) / 2)
    ax.set_yticklabels(top_depts, fontsize=11)
    ax.set_xlabel("人數", fontsize=13)
    ax.set_title("112–114 學年各系招生人數比較", fontsize=16, fontweight="bold")
    ax.legend(title="學年度", loc="lower right")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "task1.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Task 1 圖表已儲存：{path}")
    plt.close(fig)


def main():
    year_data = {}
    for year in YEARS:
        year_data[year] = load_year(year)

    top_depts = get_top_depts(year_data, top_n=8)
    print("Top depts:", top_depts)

    plot_grouped_bar(year_data, top_depts)


if __name__ == "__main__":
    main()
