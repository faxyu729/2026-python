"""
衛星距離 (Satellites) - 單元測試

題目說明：
- 地球半徑：6440 公里
- 計算兩顆衛星之間的弧長和弦長
- 弧長 = r × a (其中 a 為弧度)
- 弦長 = 2 × r × sin(a/2)

單元測試：測試角度轉換和距離計算
"""

import unittest
import math


def calculate_satellite_distance(s, angle, angle_unit):
    """
    計算衛星之間的弧長和弦長

    參數：
        s: 衛星距地表高度（公里）
        angle: 兩衛星與地心所成夾角（數值）
        angle_unit: 角度單位 ('deg' 表示度，'min' 表示分)

    返回值：
        (弧長, 弦長) 元組
    """
    # 地球半徑
    EARTH_RADIUS = 6440

    # 衛星到地心的距離（軌道半徑）
    r = EARTH_RADIUS + s

    # 將角度轉換為弧度
    if angle_unit.lower() == "deg":
        # 度轉弧度：弧度 = 度 × π / 180
        a = angle * math.pi / 180
    elif angle_unit.lower() == "min":
        # 分轉弧度：分 × (π / 180 / 60) = 分 × π / 10800
        a = angle * math.pi / 10800
    else:
        raise ValueError(f"無效的角度單位: {angle_unit}")

    # 計算弧長
    arc_length = r * a

    # 計算弦長
    chord_length = 2 * r * math.sin(a / 2)

    return arc_length, chord_length


class TestSatellites(unittest.TestCase):
    """衛星距離單元測試類別"""

    def test_angle_unit_conversion_deg(self):
        """測試 1: 度數轉弧度"""
        # 180 度 = π 弧度
        angle_rad = 180 * math.pi / 180
        self.assertAlmostEqual(angle_rad, math.pi, places=9)

    def test_angle_unit_conversion_min(self):
        """測試 2: 分數轉弧度"""
        # 60 分 = 1 度 = π/180 弧度
        angle_rad = 60 * math.pi / 10800
        expected = 1 * math.pi / 180
        self.assertAlmostEqual(angle_rad, expected, places=9)

    def test_basic_calculation_height_500_30deg(self):
        """測試 3: 高度 500km，角度 30度"""
        arc, chord = calculate_satellite_distance(500, 30, "deg")

        # 驗證：r = 6940
        r = 6440 + 500
        expected_arc = r * 30 * math.pi / 180
        expected_chord = 2 * r * math.sin(30 * math.pi / 180 / 2)

        self.assertAlmostEqual(arc, expected_arc, places=5)
        self.assertAlmostEqual(chord, expected_chord, places=5)

        print(f"高度 500km, 角度 30°: 弧長 {arc:.6f}, 弦長 {chord:.6f}")

    def test_basic_calculation_height_700_60min(self):
        """測試 4: 高度 700km，角度 60分"""
        arc, chord = calculate_satellite_distance(700, 60, "min")

        # 60 分 = 1 度
        r = 6440 + 700
        expected_arc = r * 1 * math.pi / 180
        expected_chord = 2 * r * math.sin(1 * math.pi / 180 / 2)

        self.assertAlmostEqual(arc, expected_arc, places=5)
        self.assertAlmostEqual(chord, expected_chord, places=5)

        print(f"高度 700km, 角度 60分: 弧長 {arc:.6f}, 弦長 {chord:.6f}")

    def test_question_example_1(self):
        """測試 5: 題目示例 1 (500 30 deg)"""
        arc, chord = calculate_satellite_distance(500, 30, "deg")

        # 題目預期輸出：3633.775503 3592.408346
        self.assertAlmostEqual(arc, 3633.775503, places=5)
        self.assertAlmostEqual(chord, 3592.408346, places=5)

    def test_question_example_2(self):
        """測試 6: 題目示例 2 (700 60 min)"""
        arc, chord = calculate_satellite_distance(700, 60, "min")

        # 題目預期輸出：124.616509 124.614927
        self.assertAlmostEqual(arc, 124.616509, places=5)
        self.assertAlmostEqual(chord, 124.614927, places=5)

    def test_question_example_3(self):
        """測試 7: 題目示例 3 (200 45 deg)"""
        arc, chord = calculate_satellite_distance(200, 45, "deg")

        # 題目預期輸出：5215.043805 5082.035982
        self.assertAlmostEqual(arc, 5215.043805, places=5)
        self.assertAlmostEqual(chord, 5082.035982, places=5)

    def test_zero_angle(self):
        """測試 8: 夾角為 0 度"""
        arc, chord = calculate_satellite_distance(500, 0, "deg")

        # 角度為 0，弧長和弦長都應該是 0
        self.assertAlmostEqual(arc, 0, places=9)
        self.assertAlmostEqual(chord, 0, places=9)

    def test_180_degree_angle(self):
        """測試 9: 夾角為 180 度（對面）"""
        arc, chord = calculate_satellite_distance(500, 180, "deg")

        r = 6440 + 500
        # 弧長 = r × π
        expected_arc = r * math.pi
        # 弦長 = 2r × sin(π/2) = 2r × 1 = 2r（直徑）
        expected_chord = 2 * r

        self.assertAlmostEqual(arc, expected_arc, places=5)
        self.assertAlmostEqual(chord, expected_chord, places=5)

    def test_arc_greater_than_chord(self):
        """測試 10: 驗證弧長 >= 弦長"""
        for angle in [1, 30, 45, 60, 90]:
            arc, chord = calculate_satellite_distance(500, angle, "deg")
            # 弧長應該大於等於弦長
            self.assertGreaterEqual(arc, chord)

    def test_small_angle_approximation(self):
        """測試 11: 小角度時，弧長 ≈ 弦長"""
        arc, chord = calculate_satellite_distance(500, 0.1, "deg")

        # 小角度時，sin(x) ≈ x，所以 2r×sin(a/2) ≈ r×a
        # 誤差應該很小
        relative_error = abs(arc - chord) / arc
        self.assertLess(relative_error, 0.01)  # 誤差少於 1%

    def test_different_heights(self):
        """測試 12: 不同高度的影響"""
        height1 = 100
        height2 = 1000

        arc1, chord1 = calculate_satellite_distance(height1, 30, "deg")
        arc2, chord2 = calculate_satellite_distance(height2, 30, "deg")

        # 高度越高，衛星離地心越遠，距離應該越大
        self.assertLess(arc1, arc2)
        self.assertLess(chord1, chord2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
