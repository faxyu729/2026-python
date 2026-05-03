import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# 設定繁體中文顯示
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Noto Sans CJK TC', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def plot_timing_comparison():
    """繪製函式耗時比較圖"""

    functions = ['讀取 CSV', '寫入 JSON', '讀取 JSON', '寫入 XML']
    timings = [0.002341, 0.001203, 0.000891, 0.003412]

    fig, ax = plt.subplots(figsize=(12, 7), dpi=100)

    bars = ax.bar(
        functions,
        timings,
        color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
        edgecolor='#2C3E50',
        linewidth=2.0,
        alpha=0.85,
    )

    ax.set_title('函式執行時間比較', fontsize=18, fontweight='bold', pad=18, color='#2C3E50')
    ax.set_xlabel('函式', fontsize=13, fontweight='bold', color='#2C3E50', labelpad=12)
    ax.set_ylabel('執行時間（秒）', fontsize=13, fontweight='bold', color='#2C3E50', labelpad=12)

    ax.tick_params(axis='x', labelsize=12, pad=8, colors='#2C3E50')
    ax.tick_params(axis='y', labelsize=11, colors='#2C3E50')

    for bar, timing in zip(bars, timings):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + height * 0.02,
            f'{timing:.6f} 秒',
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold',
            color='#2C3E50',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#BDC3C7', alpha=0.9, linewidth=1),
        )

    ax.grid(axis='y', alpha=0.4, linestyle='--', linewidth=0.8, color='#ECF0F1')
    ax.set_axisbelow(True)
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FFFFFF')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')

    output_dir = Path(r"E:\python\week 10\2026-python\weeks\week-10\solutions\1114405020\output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'timing_comparison.png'

    plt.subplots_adjust(top=0.88, bottom=0.16, left=0.12, right=0.98)
    plt.savefig(str(output_path), dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close(fig)

    print('圖表已儲存：' + str(output_path))


if __name__ == '__main__':
    plot_timing_comparison()
