#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 272 - TeX 引號轉換 測試程式
"""

import unittest


def convert_quotes(text):
    """轉換普通雙引號為TeX引號"""
    open_quote = True
    result = []

    for char in text:
        if char == '"':
            result.append("``" if open_quote else "''")
            open_quote = not open_quote
        else:
            result.append(char)

    return "".join(result)


class TestQuestion272(unittest.TestCase):
    def test_single_quote_pair(self):
        """測試：單個引號對"""
        result = convert_quotes('He said "Hello"')
        expected = "He said ``Hello''"
        self.assertEqual(result, expected)

    def test_multiple_quote_pairs(self):
        """測試：多個引號對"""
        result = convert_quotes('"To be" or "not to be"')
        expected = "``To be'' or ``not to be''"
        self.assertEqual(result, expected)

    def test_no_quotes(self):
        """測試：沒有引號"""
        result = convert_quotes("No quotes here")
        expected = "No quotes here"
        self.assertEqual(result, expected)

    def test_adjacent_quotes(self):
        """測試：相鄰引號"""
        result = convert_quotes('""')
        expected = "``''"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
