# Week 03 - CPE 競賽練習題組

## 概述

本週完成了5個 UVA 競賽程式問題的完整實現，包括單元測試、完整解法、簡化版本和詳細測試文檔。

## 完成的問題

### 1. QUESTION-100 - 3n+1 問題（Collatz Conjecture）

**題目描述**：計算數字範圍內的最大Cycle-length

**核心演算法**：
- 遞迴計算Cycle-length（步數計數）
- 使用記憶化優化：避免重複計算
- 時間複雜度：O(n * log m)（其中n為範圍大小）

**檔案**：
- `question100.py` - 完整解法，包含詳細中文註解
- `question100_easy.py` - 簡化版本（～90行）
- `tests/test_question100.py` - 11個單元測試
- `TEST_LOG_100.md` - 完整測試文檔
- `EASY_TEST_LOG_100.md` - 簡化版本測試文檔

**測試結果**：✅ 全部通過 (11/11 單元測試)

---

### 2. QUESTION-118 - 機器人模擬（Robots）

**題目描述**：在矩形網格中模擬機器人移動，處理掉落和Scent標記機制

**核心演算法**：
- 方向管理（N, S, E, W）和旋轉邏輯
- 邊界檢測和掉落判定
- Scent標記機制（使用集合存儲）
- 時間複雜度：O(R * L)（R為機器人數，L為指令總長）

**檔案**：
- `question118.py` - 完整解法，130行
- `question118_easy.py` - 簡化版本，52行
- `tests/test_question118.py` - 11個單元測試
- `TEST_LOG_118.md` - 完整測試文檔
- `EASY_TEST_LOG_118.md` - 簡化版本測試文檔

**測試結果**：✅ 全部通過 (11/11 單元測試)

**關鍵概念**：
- 使用方向索引簡化旋轉邏輯
- Scent標記防止重複掉落

---

### 3. QUESTION-272 - TeX 引號轉換

**題目描述**：將普通雙引號轉換為TeX方向引號（`` 和 ''）

**核心演算法**：
- 狀態機：追蹤是否在開引號狀態
- 交替輸出 `` 和 ''
- 時間複雜度：O(N)（N為文本長度）

**檔案**：
- `question272.py` - 完整解法，35行
- `question272_easy.py` - 簡化版本，6行
- `tests/test_question272.py` - 12個單元測試
- `TEST_LOG_272.md` - 完整測試文檔
- `EASY_TEST_LOG_272.md` - 簡化版本測試文檔

**測試結果**：✅ 全部通過 (12/12 單元測試)

**特點**：極簡實現，易於手寫

---

### 4. QUESTION-299 - 火車車廂排序

**題目描述**：計算通過相鄰交換將車廂排序所需的最少交換次數（逆序對計數）

**核心演算法**：
- 冒泡排序+計數
- 每次交換就累加計數器
- 時間複雜度：O(L²)（L為車廂數，最多50）

**檔案**：
- `question299.py` - 完整解法，38行
- `question299_easy.py` - 簡化版本，19行
- `tests/test_question299.py` - 12個單元測試
- `TEST_LOG_299.md` - 完整測試文檔
- `EASY_TEST_LOG_299.md` - 簡化版本測試文檔

**測試結果**：✅ 全部通過 (12/12 單元測試)

**關鍵概念**：逆序對 = 冒泡排序交換次數

---

### 5. QUESTION-490 - 文本旋轉

**題目描述**：將矩形文本順時針旋轉90度

**核心演算法**：
- 讀取所有行，填充到相同寬度
- 從右到左逐列輸出（每列從上到下讀取）
- 時間複雜度：O(N × M)（N行M列）

**檔案**：
- `question490.py` - 完整解法，42行
- `question490_easy.py` - 簡化版本，5行邏輯
- `tests/test_question490.py` - 9個單元測試
- `TEST_LOG_490.md` - 完整測試文檔
- `EASY_TEST_LOG_490.md` - 簡化版本測試文檔

**測試結果**：✅ 全部通過 (9/9 單元測試)

**特點**：使用列表推導式，代碼極簡

---

## 總體統計

| 指標 | 數值 |
|------|------|
| **完成問題數** | 5個 |
| **檔案總數** | 25個（10個解法 + 10個測試 + 5個文檔） |
| **單元測試數** | 55個 |
| **測試通過率** | 100% (55/55) |
| **總代碼行數** | ~400行 |
| **簡化版本行數** | ~150行 |

## 文件結構

```
solutions/1114405020/
├── question100.py           # QUESTION-100 完整版
├── question100_easy.py      # QUESTION-100 簡化版
├── question118.py           # QUESTION-118 完整版
├── question118_easy.py      # QUESTION-118 簡化版
├── question272.py           # QUESTION-272 完整版
├── question272_easy.py      # QUESTION-272 簡化版
├── question299.py           # QUESTION-299 完整版
├── question299_easy.py      # QUESTION-299 簡化版
├── question490.py           # QUESTION-490 完整版
├── question490_easy.py      # QUESTION-490 簡化版
├── tests/
│   ├── test_question100.py  # QUESTION-100 測試
│   ├── test_question118.py  # QUESTION-118 測試
│   ├── test_question272.py  # QUESTION-272 測試
│   ├── test_question299.py  # QUESTION-299 測試
│   └── test_question490.py  # QUESTION-490 測試
├── TEST_LOG_100.md          # QUESTION-100 測試日誌
├── TEST_LOG_118.md          # QUESTION-118 測試日誌
├── TEST_LOG_272.md          # QUESTION-272 測試日誌
├── TEST_LOG_299.md          # QUESTION-299 測試日誌
├── TEST_LOG_490.md          # QUESTION-490 測試日誌
├── EASY_TEST_LOG_100.md     # 簡化版測試日誌
├── EASY_TEST_LOG_118.md     # 簡化版測試日誌
├── EASY_TEST_LOG_272.md     # 簡化版測試日誌
├── EASY_TEST_LOG_299.md     # 簡化版測試日誌
└── EASY_TEST_LOG_490.md     # 簡化版測試日誌
```

## 測試執行方式

### 執行所有單元測試
```bash
python -m unittest discover tests/ -v
```

### 執行特定問題的測試
```bash
python -m unittest tests.test_question100 -v
```

### 運行完整解法
```bash
python question100.py < input.txt
```

### 運行簡化版本
```bash
python question100_easy.py < input.txt
```

## 設計特點

### 1. **雙版本實現**
- **完整版**：詳細中文註解，便於理解
- **簡化版**：精簡代碼，便於競賽快速手寫

### 2. **完整的單元測試**
- 邊界情況測試
- 正常情況測試
- 複雜場景測試

### 3. **詳細的文檔**
- 算法說明
- 複雜度分析
- 逐行測試結果
- 手寫複習要點

### 4. **傳統中文註解**
- 所有代碼使用繁體中文註解
- 便於中文用戶學習和理解
- 符合課程要求

## 競賽準備

### 簡化版本的用途
簡化版本經過精心設計，每個版本都是最短的可運行代碼，適合在競賽環境中：
- 快速手寫
- 減少輸入錯誤
- 保留核心邏輯

### 建議的練習方式
1. 第一遍：理解完整版本的邏輯
2. 第二遍：手寫簡化版本
3. 第三遍：在20分鐘內完成簡化版本
4. 第四遍：在競賽時直接使用

## 學習收穫

本週涵蓋的核心概念：
- ✅ 遞迴和記憶化（QUESTION-100）
- ✅ 狀態機和邊界檢測（QUESTION-118）
- ✅ 狀態追蹤（QUESTION-272）
- ✅ 排序和計數（QUESTION-299）
- ✅ 矩陣操作和坐標轉換（QUESTION-490）

## 后续步骤

- [ ] 對簡化版本進行手寫練習
- [ ] 在規定時間內完成問題（20-30分鐘/題）
- [ ] 針對容易出錯的部分重點複習
- [ ] 參考測試日誌驗證實現正確性
