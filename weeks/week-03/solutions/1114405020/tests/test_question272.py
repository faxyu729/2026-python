#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 272 - TeX 引號轉換 測試檔

測試引號轉換的各種情況：
1. 單個引號對
2. 多個引號對
3. 相鄰引號
4. 特殊字符與引號混合
5. 多行文本
"""

import unittest


class TexQuoteConverter:
    """TeX 引號轉換器"""

    @staticmethod
    def convert(text):
        """
        將普通雙引號轉換為 TeX 方向引號。

        參數：
            text (str)：輸入文本

        返回：
            str：轉換後的文本
        """
        open_quote = True
        result = []

        for char in text:
            if char == '"':
                if open_quote:
                    result.append("``")
                else:
                    result.append("''")
                open_quote = not open_quote
            else:
                result.append(char)

        return "".join(result)


class TestTexQuoteConversion(unittest.TestCase):
    """TeX 引號轉換測試類"""

    def test_single_quote_pair(self):
        """測試：單個引號對"""
        input_text = 'He said "Hello"'
        expected = "He said ``Hello''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_multiple_quote_pairs(self):
        """測試：多個引號對"""
        input_text = '"To be" or "not to be"'
        expected = "``To be'' or ``not to be''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_adjacent_quotes(self):
        """測試：相鄰引號"""
        input_text = '""'
        expected = "``''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_no_quotes(self):
        """測試：沒有引號的文本"""
        input_text = "This is a simple text without quotes"
        expected = "This is a simple text without quotes"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_special_characters(self):
        """測試：特殊字符與引號混合"""
        input_text = 'Hello, "world"!'
        expected = "Hello, ``world''!"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_nested_like_pattern(self):
        """測試：模擬嵌套樣式"""
        input_text = '"A" and "B" and "C"'
        expected = "``A'' and ``B'' and ``C''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_four_quotes(self):
        """測試：四個引號（兩對）"""
        input_text = '"One" "Two"'
        expected = "``One'' ``Two''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_quote_with_punctuation(self):
        """測試：引號與標點符號"""
        input_text = '"Hello," he said. "Goodbye," she replied.'
        expected = "``Hello,'' he said. ``Goodbye,'' she replied."
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_apostrophe_vs_quote(self):
        """測試：區分撇號與雙引號"""
        input_text = 'It\'s "beautiful"'
        expected = "It's ``beautiful''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_numbers_and_quotes(self):
        """測試：數字與引號混合"""
        input_text = 'The answer is "42" according to "Hitchhiker"'
        expected = "The answer is ``42'' according to ``Hitchhiker''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_multiline_text(self):
        """測試：多行文本"""
        input_text = '"Line 1"\n"Line 2"'
        expected = "``Line 1''\n``Line 2''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)

    def test_empty_quotes(self):
        """測試：空引號"""
        input_text = 'He said ""'
        expected = "He said ``''"
        result = TexQuoteConverter.convert(input_text)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
