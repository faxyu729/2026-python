# -*- coding: utf-8 -*-
"""
11417 GCD 總和 —— 單元測試
測試對象：11417.hand.py（手打程式）
"""

import unittest
import importlib.util
import sys
import os
import io

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "11417.hand.py")
_spec = importlib.util.spec_from_file_location("sol_11417", _path)
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


class TestGCDSum(unittest.TestCase):

    def test_n_10(self):
        """N=10 → 67"""
        self.assertEqual(run_solve("10\n0"), "67")

    def test_n_100(self):
        """N=100 → 13015"""
        self.assertEqual(run_solve("100\n0"), "13015")

    def test_n_500(self):
        """N=500 → 442011"""
        self.assertEqual(run_solve("500\n0"), "442011")

    def test_n_2(self):
        """N=2 → 1"""
        self.assertEqual(run_solve("2\n0"), "1")

    def test_multiple_inputs(self):
        """多組輸入"""
        self.assertEqual(run_solve("10\n100\n500\n0"), "67\n13015\n442011")


if __name__ == "__main__":
    unittest.main()
