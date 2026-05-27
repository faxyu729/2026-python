# -*- coding: utf-8 -*-
"""
11461 完全平方數（Square Numbers）—— 單元測試
測試對象：11461.hand.py（手打程式）
"""

import unittest
import importlib.util
import sys
import os
import io

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "11461.hand.py")
_spec = importlib.util.spec_from_file_location("sol_11461", _path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)


def run_solve(input_text):
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


class TestSquareNumbers(unittest.TestCase):

    def test_1_to_4(self):
        """[1,4] → 2"""
        self.assertEqual(run_solve("1 4\n0 0"), "2")

    def test_1_to_10(self):
        """[1,10] → 3"""
        self.assertEqual(run_solve("1 10\n0 0"), "3")

    def test_1_to_100000(self):
        """[1,100000] → 316"""
        self.assertEqual(run_solve("1 100000\n0 0"), "316")

    def test_no_square(self):
        """[10,15] → 0"""
        self.assertEqual(run_solve("10 15\n0 0"), "0")

    def test_multiple(self):
        """多組輸入"""
        data = "1 4\n1 10\n1 100000\n0 0"
        self.assertEqual(run_solve(data), "2\n3\n316")


if __name__ == "__main__":
    unittest.main()
