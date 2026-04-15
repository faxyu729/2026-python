"""
衛星距離 (Satellites) - 簡易版本

簡化說明：
直接使用數學公式計算弧長和弦長
"""

import math


def calculate_satellite_distance_easy(s, angle, angle_unit):
    """
    計算衛星之間的弧長和弦長

    簡易思路：
    1. 已知地球半徑 R = 6440 km
    2. 衛星軌道半徑 r = R + s
    3. 根據角度單位轉換為弧度
    4. 使用公式直接計算弧長和弦長

    公式：
    - 弧長（Arc Length） = r × θ (θ 為弧度)
    - 弦長（Chord Length） = 2 × r × sin(θ/2)

    參數：
        s: 衛星高度（km）
        angle: 夾角值
        angle_unit: 角度單位（'deg' 或 'min'）

    返回值：
        (弧長, 弦長) 元組
    """

    # 地球半徑（公里）
    EARTH_RADIUS = 6440

    # 衛星軌道半徑
    r = EARTH_RADIUS + s

    # 角度轉弧度
    if angle_unit.lower() == "deg":
        # 度數轉弧度：度 × π/180
        theta = angle * math.pi / 180
    elif angle_unit.lower() == "min":
        # 分數轉弧度：分 × π/10800
        # （因為 1度 = 60分，所以 1分 = π/(180×60) = π/10800）
        theta = angle * math.pi / 10800
    else:
        raise ValueError(f"無效單位: {angle_unit}")

    # 計算弧長
    arc_length = r * theta

    # 計算弦長
    chord_length = 2 * r * math.sin(theta / 2)

    return arc_length, chord_length


# 簡易測試
if __name__ == "__main__":
    print("=== 衛星距離簡易版本測試 ===\n")

    print("地球半徑: 6440 km")
    print("公式:")
    print("  衛星軌道半徑 r = 6440 + s")
    print("  弧長 = r × θ (弧度)")
    print("  弦長 = 2 × r × sin(θ/2)\n")

    # 測試用例
    test_cases = [
        (500, 30, "deg"),
        (700, 60, "min"),
        (200, 45, "deg"),
    ]

    for s, angle, unit in test_cases:
        arc, chord = calculate_satellite_distance_easy(s, angle, unit)

        print(f"高度: {s} km, 角度: {angle} {unit}")
        print(f"  弧長: {arc:.6f} km")
        print(f"  弦長: {chord:.6f} km")
        print()

    print("=" * 50)
    print("補充說明：")
    print("- 度轉弧度：乘以 π/180")
    print("- 分轉弧度：乘以 π/10800（因為 60分 = 1度）")
    print("- 弧長永遠 >= 弦長（在同一圓弧上）")
    print("- 小角度時，弧長接近弦長")
