"""
自動傘 (Umbrella) - 單元測試

題目說明：
- N 把自動傘在寬度為 W 的馬路上往返移動
- 統計 T 秒內落到馬路上的雨水體積
- 每把傘的覆蓋面積 = 傘的長度 × 馬路寬度
- 雨水體積 = 覆蓋面積 × 時間 × 單位降雨量

單元測試：測試各種傘的移動和覆蓋情況
"""

import unittest


def calculate_umbrella_coverage(n, w, t, v, umbrellas):
    """
    計算自動傘對雨水的總覆蓋體積

    參數：
        n: 傘的數量
        w: 馬路寬度
        t: 統計時間（秒）
        v: 單位面積單位時間內的降雨體積
        umbrellas: 傘的列表 [(x, l, speed), ...]

    返回值：
        落到馬路上的雨水總體積
    """
    total_volume = 0.0

    # 採用時間切片法來計算
    # 將時間分割成足夠細的時間片段，以提高精度
    time_slice = 0.01  # 時間片段（秒）

    # 計算時間片段的數量
    num_slices = int(t / time_slice) + 1

    # 遍歷每個時間片段
    for slice_idx in range(num_slices):
        current_time = slice_idx * time_slice

        # 不超過統計時間
        if current_time >= t:
            current_time = t

        # 計算當前時間段的覆蓋長度
        covered_length = 0.0

        # 遍歷每把傘
        for x, l, speed in umbrellas:
            # 計算傘在當前時間的位置
            if speed == 0:
                # 靜止不動
                left = x
                right = x + l
            else:
                # 計算傘的移動距離
                distance = speed * current_time

                # 計算傘的往返週期
                period = 2 * (w - l) / abs(speed)

                # 計算週期內的位置
                relative_distance = distance % period

                if relative_distance <= w - l:
                    # 向右移動的階段
                    left = x + relative_distance
                else:
                    # 向左移動的階段
                    left = x + 2 * (w - l) - relative_distance

                right = left + l

            # 計算傘的實際覆蓋區間（限制在 [0, w] 範圍內）
            left = max(0, left)
            right = min(w, right)

            if left < right:
                covered_length += right - left

        # 計算本時間片段的雨水體積
        if slice_idx < num_slices - 1:
            delta_time = time_slice
        else:
            delta_time = t - current_time

        volume_in_slice = covered_length * w * v * delta_time
        total_volume += volume_in_slice

    return total_volume


def calculate_umbrella_coverage_simple(n, w, t, v, umbrellas):
    """
    簡化版本：使用積分方法計算總體積
    """
    total_volume = 0.0

    # 計算所有傘在時間 t 內覆蓋的總長度×時間
    for x, l, speed in umbrellas:
        if speed == 0:
            # 靜止傘：始終覆蓋長度 l
            coverage = min(l, w)  # 傘不超過馬路寬度
            total_volume += coverage * w * v * t
        else:
            # 移動傘：計算往返一個週期的距離
            period = 2 * (w - l) / abs(speed)

            # 在時間 t 內完成的週期數
            complete_cycles = int(t / period)
            remaining_time = t - complete_cycles * period

            # 每個完整週期內的覆蓋距離
            coverage_per_cycle = (w - l) * 2

            # 完整週期的體積
            cycle_volume = (
                (coverage_per_cycle / period) * w * v * complete_cycles * period
            )

            # 剩餘時間的覆蓋
            remaining_distance = abs(speed) * remaining_time
            if remaining_distance > w - l:
                remaining_distance = w - l + (remaining_distance - (w - l))

            remaining_volume = (
                (remaining_distance / remaining_time if remaining_time > 0 else 0)
                * w
                * v
                * remaining_time
            )

            total_volume += cycle_volume + remaining_volume

    return total_volume


class TestUmbrella(unittest.TestCase):
    """自動傘單元測試類別"""

    def test_single_stationary_umbrella(self):
        """測試 1: 單把靜止的傘"""
        # 1 把傘，馬路寬 10，時間 5，降雨量 2
        # 傘長 5，靜止不動
        # 體積 = 5 * 10 * 2 * 5 = 500
        n, w, t, v = 1, 10, 5, 2
        umbrellas = [(0, 5, 0)]

        result = calculate_umbrella_coverage(n, w, t, v, umbrellas)
        # 允許一定誤差
        self.assertAlmostEqual(result, 500.0, places=0)

    def test_multiple_stationary_umbrellas(self):
        """測試 2: 多把靜止傘，不重疊"""
        # 2 把傘，馬路寬 10，時間 10，降雨量 1
        # 傘1：位置 0，長 3
        # 傘2：位置 5，長 3
        # 總體積 = (3+3) * 10 * 1 * 10 = 600
        n, w, t, v = 2, 10, 10, 1
        umbrellas = [(0, 3, 0), (5, 3, 0)]

        result = calculate_umbrella_coverage(n, w, t, v, umbrellas)
        self.assertAlmostEqual(result, 600.0, places=0)

    def test_moving_umbrella(self):
        """測試 3: 移動傘"""
        # 1 把傘，馬路寬 10，時間 1，降雨量 1
        # 傘長 5，速度 5（向右移動）
        n, w, t, v = 1, 10, 1, 1
        umbrellas = [(0, 5, 5)]

        result = calculate_umbrella_coverage(n, w, t, v, umbrellas)
        # 應該有正的體積
        self.assertGreater(result, 0)

    def test_zero_length_umbrella(self):
        """測試 4: 長度為 0 的傘（邊界情況）"""
        n, w, t, v = 1, 10, 5, 2
        umbrellas = [(0, 0, 0)]

        result = calculate_umbrella_coverage(n, w, t, v, umbrellas)
        self.assertEqual(result, 0.0)

    def test_zero_time(self):
        """測試 5: 時間為 0"""
        n, w, t, v = 1, 10, 0, 2
        umbrellas = [(0, 5, 0)]

        result = calculate_umbrella_coverage(n, w, t, v, umbrellas)
        self.assertEqual(result, 0.0)

    def test_zero_rainfall(self):
        """測試 6: 降雨量為 0"""
        n, w, t, v = 1, 10, 5, 0
        umbrellas = [(0, 5, 0)]

        result = calculate_umbrella_coverage(n, w, t, v, umbrellas)
        self.assertEqual(result, 0.0)

    def test_umbrella_exceeds_width(self):
        """測試 7: 傘長度超過馬路寬度"""
        # 傘長度大於馬路寬度，應該限制到馬路寬度
        n, w, t, v = 1, 10, 5, 1
        umbrellas = [(0, 15, 0)]  # 傘長 15，馬路寬 10

        result = calculate_umbrella_coverage(n, w, t, v, umbrellas)
        # 體積應該 <= 10 * 10 * 1 * 5 = 500
        self.assertLessEqual(result, 500.0)

    def test_negative_velocity(self):
        """測試 8: 向左移動的傘（負速度）"""
        n, w, t, v = 1, 10, 1, 1
        umbrellas = [(5, 3, -2)]  # 向左移動

        result = calculate_umbrella_coverage(n, w, t, v, umbrellas)
        self.assertGreater(result, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
