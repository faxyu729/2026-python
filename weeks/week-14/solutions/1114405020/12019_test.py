# -*- coding: utf-8 -*-
"""
12019 Doom's Day 演算法 —— 單元測試
測試對象：12019.hand.py（手打程式）
"""

import unittest
import importlib.util
import sys
import os
import io

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "12019.hand.py")
_spec = importlib.util.spec_from_file_location("sol_12019", _path)
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


class TestDoomsDay(unittest.TestCase):

    def test_jan_doomsday(self):
        """1 月 10 日 → Wednesday"""
        self.assertEqual(run_solve("1\n1 10"), "Wednesday")

    def test_two_doomsdays(self):
        """1/10 和 2/21 → Wednesday"""
        self.assertEqual(run_solve("2\n1 10\n2 21"), "Wednesday\nWednesday")

    def test_various(self):
        """多組不同日期"""
        # 1/1: Mon, 12/25: Tue, 7/4: Wed
        self.assertEqual(run_solve("3\n1 1\n12 25\n7 4"),
                         "Monday\nTuesday\nWednesday")

    def test_dec_25(self):
        """12 月 25 日 → Tuesday"""
        self.assertEqual(run_solve("1\n12 25"), "Tuesday")


if __name__ == "__main__":
    unittest.main()
