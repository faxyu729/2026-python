# -*- coding: utf-8 -*-
"""
UVA 11063 — RGB 轉 XYZ 色彩空間（手打程式）

題目：將 n×n 影像中的每個像素從 RGB 色彩轉換到 XYZ 色彩，
      並計算所有像素的平均亮度（Y 的平均值）。
"""

def rgb_to_xyz(r, g, b):
    """將單一 RGB 像素轉換為 XYZ，回傳 (X, Y, Z) 元組"""
    x = 0.5149 * r + 0.3244 * g + 0.1607 * b
    y = 0.2654 * r + 0.6704 * g + 0.0642 * b
    z = 0.0248 * r + 0.1248 * g + 0.8504 * b
    return (round(x, 4), round(y, 4), round(z, 4))


def solve_all(input_data):
    """解析輸入，處理所有像素，回傳完整輸出字串"""
    lines = input_data.strip().splitlines()
    n = int(lines[0].strip())
    y_values = []
    output_lines = []
    line_idx = 1
    for _ in range(n):
        row = lines[line_idx].strip().split()
        line_idx += 1
        for i in range(0, len(row), 3):
            r = int(row[i])
            g = int(row[i + 1])
            b = int(row[i + 2])
            x, y, z = rgb_to_xyz(r, g, b)
            y_values.append(y)
            output_lines.append(f"{x:.4f} {y:.4f} {z:.4f}")
    avg_y = sum(y_values) / len(y_values)
    output_lines.append(f"The average of Y is {avg_y:.4f}")
    return "\n".join(output_lines)


def main():
    """主程式：從標準輸入讀取資料並輸出結果"""
    import sys
    data = sys.stdin.read()
    print(solve_all(data))


if __name__ == "__main__":
    main()
