"""
自動傘 (Umbrella) - 簡易版本

簡化說明：
使用更直觀的方式計算傘的覆蓋區域
"""


def calculate_umbrella_volume_easy(n, w, t, v, umbrellas):
    """
    計算傘對雨水的覆蓋體積

    簡易思路：
    1. 建立時間軸，分割成若干時間點
    2. 對每個時間點，計算所有傘的覆蓋長度
    3. 對時間積分得到總體積

    參數：
        n: 傘的數量
        w: 馬路寬度
        t: 統計時間（秒）
        v: 單位面積單位時間的降雨量
        umbrellas: 傘的列表 [(起始位置, 長度, 速度), ...]

    返回值：
        雨水總體積
    """
    # 將時間分割成小片段，提高精度
    dt = 0.01  # 時間片段
    total_volume = 0.0

    # 遍歷每個時間片段
    current_time = 0.0
    while current_time < t:
        # 計算當前時間的覆蓋長度
        covered_length = 0.0

        # 檢查每把傘
        for start_pos, length, speed in umbrellas:
            # 計算傘的當前位置
            if speed == 0:
                # 靜止傘
                left = start_pos
                right = start_pos + length
            else:
                # 移動傘
                # 計算往返週期
                period = 2 * (w - length) / abs(speed)

                # 計算當前時間在週期中的位置
                time_in_cycle = current_time % period

                # 計算移動距離
                if time_in_cycle <= (w - length) / abs(speed):
                    # 向右移動階段
                    distance = speed * time_in_cycle
                    left = start_pos + distance
                else:
                    # 向左移動階段
                    distance = (w - length) - speed * (
                        time_in_cycle - (w - length) / abs(speed)
                    )
                    left = start_pos + distance

                right = left + length

            # 限制在馬路範圍內
            left = max(0, left)
            right = min(w, right)

            # 累加覆蓋長度
            if left < right:
                covered_length += right - left

        # 計算本時間片段的體積
        volume_in_dt = covered_length * w * v * dt
        total_volume += volume_in_dt

        current_time += dt

    return total_volume


# 簡易測試
if __name__ == "__main__":
    print("=== 自動傘簡易版本測試 ===\n")

    # 測試 1：單把靜止傘
    print("測試 1：單把靜止傘")
    n, w, t, v = 1, 10, 5, 2
    umbrellas = [(0, 5, 0)]
    result = calculate_umbrella_volume_easy(n, w, t, v, umbrellas)
    print(f"馬路寬度: {w}m, 傘長: 5m, 時間: {t}s, 降雨量: {v}")
    print(f"預期體積: 500 (= 5*10*2*5)")
    print(f"計算結果: {result:.2f}\n")

    # 測試 2：多把靜止傘
    print("測試 2：多把靜止傘（不重疊）")
    n, w, t, v = 2, 10, 10, 1
    umbrellas = [(0, 3, 0), (5, 3, 0)]
    result = calculate_umbrella_volume_easy(n, w, t, v, umbrellas)
    print(f"傘 1：位置 0，長度 3m")
    print(f"傘 2：位置 5，長度 3m")
    print(f"預期體積: 600 (= (3+3)*10*1*10)")
    print(f"計算結果: {result:.2f}\n")

    # 測試 3：零時間
    print("測試 3：零時間")
    n, w, t, v = 1, 10, 0, 2
    umbrellas = [(0, 5, 0)]
    result = calculate_umbrella_volume_easy(n, w, t, v, umbrellas)
    print(f"時間: {t}s")
    print(f"預期體積: 0")
    print(f"計算結果: {result:.2f}\n")

    # 測試 4：零降雨量
    print("測試 4：零降雨量")
    n, w, t, v = 1, 10, 5, 0
    umbrellas = [(0, 5, 0)]
    result = calculate_umbrella_volume_easy(n, w, t, v, umbrellas)
    print(f"降雨量: {v}")
    print(f"預期體積: 0")
    print(f"計算結果: {result:.2f}")
