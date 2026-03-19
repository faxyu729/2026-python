# Week 03 - CPE 競賽題組

## 📋 專案概述

本專案包含5個UVA競賽題的完整實現，每題都有：
- ✅ **AI簡化版** - 含詳細中文註解
- ✅ **手打版本** - 自己實現的版本  
- ✅ **測試程式** - 單元測試
- ✅ **測試LOG** - 手打版本的執行結果

## 📁 檔案結構

```
solutions/1114405020/
├── question100_ai_easy.py         ← AI簡化版 (有中文註解)
├── question100_hand.py            ← 手打版本
├── question118_ai_easy.py
├── question118_hand.py
├── question272_ai_easy.py
├── question272_hand.py
├── question299_ai_easy.py
├── question299_hand.py
├── question490_ai_easy.py
├── question490_hand.py
├── tests/
│   ├── test_question100.py        ← 測試程式
│   ├── test_question118.py
│   ├── test_question272.py
│   ├── test_question299.py
│   └── test_question490.py
├── HAND_TEST_LOG_100.md           ← 手打版本測試LOG
├── HAND_TEST_LOG_118.md
├── HAND_TEST_LOG_272.md
├── HAND_TEST_LOG_299.md
├── HAND_TEST_LOG_490.md
└── README.md                       ← 本檔案
```

## 🎯 五個問題概覽

### QUESTION-100 - 3n+1 問題
- **演算法**：遞迴 + 記憶化
- **關鍵概念**：Cycle-length計算
- **測試狀態**：✅ 全部通過

### QUESTION-118 - 機器人模擬
- **演算法**：狀態管理 + 邊界檢測
- **關鍵概念**：Scent標記機制
- **測試狀態**：✅ 全部通過

### QUESTION-272 - TeX 引號轉換
- **演算法**：狀態機
- **關鍵概念**：交替輸出 `` 和 ''
- **測試狀態**：✅ 全部通過

### QUESTION-299 - 火車車廂排序
- **演算法**：冒泡排序計數
- **關鍵概念**：逆序對計數
- **測試狀態**：✅ 全部通過

### QUESTION-490 - 文本旋轉
- **演算法**：矩陣旋轉
- **關鍵概念**：坐標轉換
- **測試狀態**：✅ 全部通過

## ✅ 測試結果

| 題目 | AI版 | 手打版 | 測試數 | 通過率 |
|------|------|--------|--------|--------|
| QUESTION-100 | ✅ | ✅ | 7 | 100% |
| QUESTION-118 | ✅ | ✅ | 5 | 100% |
| QUESTION-272 | ✅ | ✅ | 4 | 100% |
| QUESTION-299 | ✅ | ✅ | 4 | 100% |
| QUESTION-490 | ✅ | ✅ | 4 | 100% |

**總計**：24個測試 / 100% 通過

## 🚀 快速開始

### 執行測試
```bash
# 執行所有測試
python -m unittest discover tests/ -v

# 執行特定問題的測試
python -m unittest tests.test_question100 -v
```

### 執行程式
```bash
# 執行手打版本
python question100_hand.py < input.txt

# 執行AI簡化版
python question100_ai_easy.py < input.txt
```

## 📝 使用說明

### AI簡化版本 (*_ai_easy.py)
- 包含詳細的中文註解
- 展示最簡潔的實現方式
- 適合學習和理解核心邏輯

### 手打版本 (*_hand.py)
- 自己實現的版本
- 邏輯與AI版相同
- 用於練習和驗證

### 測試程式 (test_*.py)
- 單元測試覆蓋核心功能
- 所有測試均通過

### 測試LOG (HAND_TEST_LOG_*.md)
- 記錄了手打版本的測試結果
- 展示了測試項目和通過狀態

## 💡 學習要點

1. **QUESTION-100**：遞迴與記憶化的應用
2. **QUESTION-118**：狀態管理和邊界條件
3. **QUESTION-272**：簡單的狀態機實現
4. **QUESTION-299**：排序算法應用
5. **QUESTION-490**：矩陣操作和坐標轉換

## 🔄 版本對比

| 方面 | AI簡化版 | 手打版 |
|------|---------|--------|
| 中文註解 | ✅ 詳細 | ✅ 基本 |
| 代碼行數 | 精簡 | 精簡 |
| 可讀性 | 高 | 高 |
| 邏輯相同 | ✅ | ✅ |

## 📌 注意事項

- 所有程式都已經過充分測試
- 手打版本與AI版本的邏輯完全相同
- 測試檔案包含了主要功能的驗證

## 📧 聯絡方式

學號：1114405020
姓名：范芯瑜
提交日期：2026年3月19日
