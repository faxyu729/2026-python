# -*- coding: utf-8 -*-
"""
11349 對稱矩陣（Symmetric Matrix）—— 單元測試
測試對象：11349.hand.py（手打程式）
"""

import unittest
import importlib.util
import sys
import os
import io

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "11349.hand.py")
_spec = importlib.util.spec_from_file_location("sol_11349", _path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)


def run_solve(input_text):
    """呼叫 solve() 並回傳輸出文字"""
    sys.stdin = io.StringIO(input_text)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    try:
        _sol.solve()
    except SystemExit:
        pass
    sys.stdout = old_stdout
    sys.stdin = sys.__stdin__
    return out.getvalue().strip()


class TestSymmetricMatrix(unittest.TestCase):

    def test_symmetric_example(self):
        """範例：第一個對稱、第二個非對稱"""
        data = "2\nN = 3\n5 1 3\n2 0 2\n3 1 5\nN = 3\n5 1 3\n2 0 2\n0 1 5"
        expected = "Test #1: Symmetric.\nTest #2: Non-symmetric."
        self.assertEqual(run_solve(data), expected)

    def test_all_symmetric(self):
        """全部對稱"""
        data = "1\nN = 2\n1 2\n2 1"
        self.assertEqual(run_solve(data), "Test #1: Symmetric.")

    def test_negative_number(self):
        """包含負數 → 非對稱"""
        data = "1\nN = 2\n1 -2\n-2 1"
        self.assertEqual(run_solve(data), "Test #1: Non-symmetric.")

    def test_single_element(self):
        """1×1 矩陣 → 對稱"""
        data = "1\nN = 1\n5"
        self.assertEqual(run_solve(data), "Test #1: Symmetric.")


if __name__ == "__main__":
    unittest.main()
