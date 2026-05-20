# -*- coding: utf-8 -*-
"""
UVA 11063 單元測試程式

測試方式：使用 importlib 載入同目錄下的 11063.py 進行測試。
"""

import unittest
import importlib.util
import os


def load_solution(name):
    """載入以數字開頭的 Python 解答模組"""
    path = os.path.join(os.path.dirname(__file__), f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"p{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = load_solution("11063_hand")
rgb_to_xyz = mod.rgb_to_xyz
solve_all = mod.solve_all


class Test11063(unittest.TestCase):
    """UVA 11063 單元測試"""

    def test_rgb_to_xyz_white(self):
        """白色 (255, 255, 255) 的對應值"""
        x, y, z = rgb_to_xyz(255, 255, 255)
        self.assertAlmostEqual(x, 255.0, delta=0.1)
        self.assertAlmostEqual(y, 255.0, delta=0.1)
        self.assertAlmostEqual(z, 255.0, delta=0.1)

    def test_rgb_to_xyz_black(self):
        """黑色 (0, 0, 0) 全部為 0"""
        x, y, z = rgb_to_xyz(0, 0, 0)
        self.assertEqual(x, 0.0)
        self.assertEqual(y, 0.0)
        self.assertEqual(z, 0.0)

    def test_rgb_to_xyz_red(self):
        """純紅 (255, 0, 0)"""
        x, y, z = rgb_to_xyz(255, 0, 0)
        self.assertAlmostEqual(x, 0.5149 * 255, delta=0.01)
        self.assertAlmostEqual(y, 0.2654 * 255, delta=0.01)
        self.assertAlmostEqual(z, 0.0248 * 255, delta=0.01)

    def test_rgb_to_xyz_green(self):
        """純綠 (0, 255, 0)"""
        x, y, z = rgb_to_xyz(0, 255, 0)
        self.assertAlmostEqual(x, 0.3244 * 255, delta=0.01)
        self.assertAlmostEqual(y, 0.6704 * 255, delta=0.01)
        self.assertAlmostEqual(z, 0.1248 * 255, delta=0.01)

    def test_sample(self):
        """範例測試：簡單的 2×2 影像"""
        sample = """2
0 0 0 100 100 100
200 200 200 255 255 255
"""
        out = solve_all(sample)
        self.assertIn("The average of Y is", out)

    def test_rounding(self):
        """驗證四捨五入至小數第 4 位"""
        x, y, z = rgb_to_xyz(100, 150, 200)
        expected_x = round(0.5149 * 100 + 0.3244 * 150 + 0.1607 * 200, 4)
        expected_y = round(0.2654 * 100 + 0.6704 * 150 + 0.0642 * 200, 4)
        expected_z = round(0.0248 * 100 + 0.1248 * 150 + 0.8504 * 200, 4)
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)
        self.assertEqual(z, expected_z)


if __name__ == "__main__":
    unittest.main()
