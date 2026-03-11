# Week 03 Solution - 1114405020

## 題目
UVA 100 - Collatz conjecture cycle length 計算與區間最大值。

## 程式檔案
- `uva100.py`：包含 cycle_length、max_cycle_length 等函式及命令列介面。
- `uva100_easy.py`：更簡單、容易記憶的版本（檔名後加上 `-easy`），使用迴圈而非遞迴。

## 測試執行
```
python -m unittest discover -s tests -p "test_*.py" -v
```

兩個版本的功能皆通過測試。

## 備註
註解以繁體中文撰寫，並使用簡單的快取機制加速計算。
