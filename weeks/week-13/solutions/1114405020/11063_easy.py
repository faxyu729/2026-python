# -*- coding: utf-8 -*-
"""
UVA 11063 — RGB 轉 XYZ 色彩空間（簡易版本）

核心概念超級簡單：
1. 給定 R, G, B 三個數字
2. 帶入三條公式算出 X, Y, Z
3. 四捨五入到小數第 4 位
4. 最後算所有 Y 的平均值

解題口訣：「帶公式 → 四捨五入 → 算平均亮度」
"""

def rgb_to_xyz(r, g, b):
    """
    把 RGB 轉成 XYZ。
    
    - r, g, b: 0~255 的整數
    - 回傳: (x, y, z) 三個四捨五入到小數第 4 位的浮點數
    """
    # === 代入三條轉換公式 ===
    x = 0.5149 * r + 0.3244 * g + 0.1607 * b
    y = 0.2654 * r + 0.6704 * g + 0.0642 * b
    z = 0.0248 * r + 0.1248 * g + 0.8504 * b
    
    # === 四捨五入到小數第 4 位 ===
    return (round(x, 4), round(y, 4), round(z, 4))


def process_pixels(pixels):
    """
    處理一組像素並輸出結果。
    
    - pixels: 串列，每個元素是 (r, g, b) 元組
    - 回傳: (輸出行的串列, 平均亮度)
    """
    y_values = []      # 存放所有 Y 值，用來算平均
    output = []
    
    for r, g, b in pixels:
        x, y, z = rgb_to_xyz(r, g, b)
        y_values.append(y)
        output.append(f"{x:.4f} {y:.4f} {z:.4f}")
    
    avg_y = sum(y_values) / len(y_values)
    output.append(f"The average of Y is {avg_y:.4f}")
    
    return output


import unittest


class Test11063Easy(unittest.TestCase):
    """UVA 11063 簡易版測試"""

    def test_black(self):
        """黑色 (0,0,0) → (0,0,0)"""
        self.assertEqual(rgb_to_xyz(0, 0, 0), (0.0, 0.0, 0.0))

    def test_white(self):
        """白色 (255,255,255) → 各分量約 255"""
        x, y, z = rgb_to_xyz(255, 255, 255)
        self.assertAlmostEqual(x, 255.0, delta=0.1)
        self.assertAlmostEqual(y, 255.0, delta=0.1)
        self.assertAlmostEqual(z, 255.0, delta=0.1)

    def test_red(self):
        """紅色 (255,0,0) 驗算"""
        x, y, z = rgb_to_xyz(255, 0, 0)
        self.assertAlmostEqual(x, 131.2995, delta=0.01)
        self.assertAlmostEqual(y, 67.677, delta=0.01)
        self.assertAlmostEqual(z, 6.324, delta=0.01)

    def test_two_pixels(self):
        """兩個像素的處理流程"""
        pixels = [(0, 0, 0), (255, 255, 255)]
        result = process_pixels(pixels)
        self.assertEqual(len(result), 3)
        self.assertIn("The average of Y is", result[-1])


if __name__ == "__main__":
    unittest.main()
