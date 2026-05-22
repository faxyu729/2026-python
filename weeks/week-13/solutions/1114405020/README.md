# Week 13 回家作業 — 招生資料視覺化分析

## 學號

1114405020

## 檔案結構

```
solutions/1114405020/
├── task1_grouped_bar.py       # Task 1：三年並排長條圖
├── task2_zipcode_heatmap.py   # Task 2：來源縣市熱力圖
├── output/
│   ├── task1.png
│   └── task2.png
├── tests/
│   ├── test_task1.py
│   └── test_task2.py
├── TEST_LOG.md
├── REPORT.md
├── AI_USAGE.md
└── README.md
```

## 執行方式

```bash
# 產生圖表
python task1_grouped_bar.py
python task2_zipcode_heatmap.py

# 執行測試
python -m unittest discover -s tests -p "test_*.py" -v
```

## 相依套件

- matplotlib
- numpy
