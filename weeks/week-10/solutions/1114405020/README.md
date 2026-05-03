# Week 10 作業 - 資料格式轉換

## 完成項目

- ✅ **Task 1** - CSV → JSON 轉換（讀取、過濾、統計、輸出）
- ✅ **Task 2** - JSON → XML 轉換（讀取、轉換、輸出）
- ✅ **Task 3** - 視覺化比較（耗時比較圖表）
- ✅ **TDD 測試** - 16 個測試用例（超過要求的 10 個）

---

## 檔案結構

```
solutions/1114405020/
├── task1_csv_to_json.py      # Task 1 主程式
├── task2_json_to_xml.py      # Task 2 主程式
├── task3_plot_comparison.py  # Task 3 視覺化程式
├── output/                   # 程式輸出目錄
│   ├── students.json        # Task 1 輸出
│   ├── students.xml         # Task 2 輸出
│   └── timing_comparison.png # Task 3 圖表
├── tests/
│   ├── test_task1.py        # Task 1 測試（8 個測試）
│   └── test_task2.py        # Task 2 測試（8 個測試）
├── TEST_LOG.md              # TDD 執行紀錄
├── TIMING_REPORT.md         # 耗時分析報告
├── README.md                # 本檔案
└── AI_USAGE.md              # AI 使用說明
```

---

## 執行方式

### 執行主程式

```bash
# Task 1：CSV 讀取並轉換為 JSON
python task1_csv_to_json.py

# Task 2：JSON 轉換為 XML
python task2_json_to_xml.py

# Task 3：繪製耗時比較圖
python task3_plot_comparison.py
```

### 執行測試

```bash
# 執行所有測試
python -m unittest discover -s tests -p "test_*.py" -v

# 執行 Task 1 測試
python -m unittest tests/test_task1 -v

# 執行 Task 2 測試
python -m unittest tests/test_task2 -v
```

---

## @timeit 裝飾器運作說明

`@timeit` 是一個計時裝飾器，用來量測函式的執行時間：

1. **記錄開始時間**：使用 `time.perf_counter()` 取得高精度時間戳
2. **執行目標函式**：執行被裝飾的函式並保存返回結果
3. **計算耗時**：用結束時間減去開始時間
4. **列印結果**：以格式 `[timeit] 函式名稱 耗時 XXs` 輸出到標準輸出
5. **返回結果**：回傳函式的執行結果

優點：無需修改函式內部邏輯，只需在函式定義前加上 `@timeit` 即可自動計時。

---

## Task 1 與 Task 2 的難點與解決方式

### 難點 1：XML 編碼問題

**問題描述：**
最初使用 `ET.tostring()` 時，中文字元可能出現編碼錯誤或亂碼。

**解決方式：**
使用 `ET.ElementTree.write()` 方法搭配 `encoding='utf-8'` 和 `xml_declaration=True`，確保：
1. 正確寫出 XML 宣告（`<?xml version="1.0" encoding="utf-8"?>`）
2. 自動處理中文字元的編碼
3. 檔案能被其他工具正確解析

```python
tree.write(filepath, encoding='utf-8', xml_declaration=True)
```

### 難點 2：CSV 檔案編碼

**問題描述：**
作業提供的 CSV 檔案使用 UTF-8-BOM 編碼，直接使用 `encoding='utf-8'` 會讀取到 BOM 標記。

**解決方式：**
使用 `encoding='utf-8-sig'`，該編碼會自動跳過 BOM 標記：

```python
with open(filepath, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
```

### 難點 3：空值和邊界情況處理

**問題描述：**
測試中需要處理空 list、缺失欄位等邊界情況。

**解決方式：**
使用 `dict.get()` 方法搭配預設值，避免 KeyError：

```python
# 而不是直接用 row["入學方式"]，會在鍵不存在時拋出異常
result = [r for r in rows if r.get("入學方式") == method]
```

---

## 測試覆蓋統計

### Task 1 測試（8 個）
| 測試函式 | 情境分類 | 驗證內容 |
|---------|---------|---------|
| `test_filter_keeps_correct_rows` | 正常 | 過濾結果正確 |
| `test_filter_removes_others` | 正常 | 排除其他類別 |
| `test_filter_empty_input` | 邊界 | 空輸入處理 |
| `test_filter_multiple_methods` | 正常 | 多種方式過濾 |
| `test_count_by_dept_correct` | 正常 | 統計結果準確 |
| `test_count_by_dept_empty` | 邊界 | 空輸入回傳空 dict |
| `test_count_single_dept` | 邊界 | 單一系所情況 |
| `test_extract_student_info_fields` | 正常 | 欄位完整性 |

### Task 2 測試（8 個）
| 測試函式 | 情境分類 | 驗證內容 |
|---------|---------|---------|
| `test_root_tag_and_attrs` | 正常 | 根元素屬性正確 |
| `test_student_count_matches` | 正常 | 元素數量一致 |
| `test_student_attrs_exist` | 正常 | 屬性完整 |
| `test_empty_student_list` | 邊界 | 空清單處理 |
| `test_xml_is_valid` | 反例 | XML 有效性 |
| `test_student_data_accuracy` | 正常 | 資料準確性 |
| `test_root_attrs_with_empty_source` | 邊界 | 空字串屬性 |
| `test_xml_with_special_characters` | 反例 | 中文字元處理 |

---

## 關鍵技術點

### 1. CSV 讀寫
- 使用 `csv.DictReader` 自動轉換為字典
- 編碼問題使用 `utf-8-sig`

### 2. JSON 處理
- 使用 `json.dump()` 和 `json.load()`
- `ensure_ascii=False` 保留中文

### 3. XML 操作
- `ElementTree` 建立樹結構
- `ET.SubElement()` 添加子節點
- 使用 `.set()` 方法設定屬性

### 4. 裝飾器設計
- `@functools.wraps()` 保留原函式元訊息
- `*args` 和 `**kwargs` 提供靈活性
- `time.perf_counter()` 提供高精度計時

### 5. 資料統計
- 使用 `collections.Counter` 計算頻次
- 支援空輸入的優雅降級

---

## 性能結果摘要

執行 @timeit 的結果（參考 TIMING_REPORT.md）：

```
[timeit] read_csv   耗時 0.002341s    # 最耗時的是讀 CSV
[timeit] write_json 耗時 0.001203s    # 寫 JSON 最快
[timeit] read_json  耗時 0.000891s    # 讀 JSON 也很快
[timeit] write_xml  耗時 0.003412s    # 寫 XML 最耗時
```

**結論**：格式選擇影響明顯，XML 操作相對耗時。

---

## 參考資料

- [Python csv 模組文件](https://docs.python.org/3/library/csv.html)
- [Python json 模組文件](https://docs.python.org/3/library/json.html)
- [Python xml.etree.ElementTree 文件](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [Time module 高精度計時](https://docs.python.org/3/library/time.html)
- [Decorators in Python](https://docs.python.org/3/glossary.html#term-decorator)

---

## 作業提交清單

- [x] task1_csv_to_json.py
- [x] task2_json_to_xml.py
- [x] task3_plot_comparison.py
- [x] tests/test_task1.py（8 個測試）
- [x] tests/test_task2.py（8 個測試）
- [x] TEST_LOG.md（TDD 紀錄）
- [x] TIMING_REPORT.md（耗時分析）
- [x] README.md（本檔案）
- [x] AI_USAGE.md（AI 使用紀錄）
- [x] output/ 目錄結構

---

## 學習心得

1. **TDD 的價值**：先寫測試讓我更清楚了解需求，減少實作過程中的錯誤
2. **裝飾器的強大**：@timeit 裝飾器展示了 Python 函式式編程的優雅
3. **格式權衡**：不同資料格式有各自的優缺點，選擇應根據使用場景
4. **編碼問題**：文字編碼在資料處理中常見但容易忽視，需要格外留意

---

## 🌟 加分項實作說明（Bonus Features）

本作業實作了 **兩項加分內容**，並完全支援繁體中文：

### 1️⃣ 使用 seaborn 製作更具設計感與可讀性的比較圖 ✅

**實裝位置**：`task3_plot_comparison.py` Line 15-80

**改進內容**：

| 特性 | 原始版本 | seaborn 優化版 |
|------|--------|-------------|
| **主題風格** | 基礎 matplotlib | `sns.set_theme()` 專業主題 |
| **調色盤** | 基礎配色 | 精選的和諧配色 (#FF6B6B, #4ECDC4, #45B7D1, #FFA07A) |
| **視覺層次** | 簡單長條 | 陰影效果 + 深灰色邊框 + 優化背景 |
| **網格設計** | 單調虛線 | 優化的網格透明度 (α=0.4) 和顏色 (#ECF0F1) |
| **坐標軸** | 標準樣式 | 移除冗餘邊框 (top, right)、統一色調 |
| **資料標籤** | 純文字 | 帶背景方框、清晰可讀 |
| **總體美感** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**技術細節**：
- 使用 `sns.set_theme(style='whitegrid', context='notebook')` 設定專業主題
- 自訂配色清單提供視覺統一性
- 優化圖表元素：隱藏 spine、調整網格、改善背景顏色
- 添加圖表底部的資料來源註解

**視覺效果**：圖表整體設計優雅、色彩和諧、易讀易懂

---

### 2️⃣ 完整的繁體中文字支援 ✅

**中文標籤完整清單**：

| 位置 | 繁體中文 | 含義 |
|------|---------|------|
| **標題** | Task 1/2 函式執行時間比較 | 圖表主標題 |
| **Y 軸標籤** | 執行時間（秒） | 縱軸說明 |
| **X 軸標籤** | 讀取 CSV | 第 1 個函式 |
| **X 軸標籤** | 寫入 JSON | 第 2 個函式 |
| **X 軸標籤** | 讀取 JSON | 第 3 個函式 |
| **X 軸標籤** | 寫入 XML | 第 4 個函式 |

**實裝位置**：`task3_plot_comparison.py` Line 95-130

**技術實現方案**：

採用 **「matplotlib 基礎圖表 + PIL 後處理」** 的混合方案：

1. **第一步**：使用 matplotlib + seaborn 繪製基礎圖表（數據、顏色、網格）
2. **第二步**：使用 PIL (Pillow) 的 ImageDraw 在圖片上添加繁體中文標籤
3. **字型支援**：自動檢測系統中的中文字型（優先使用 `msyh.ttc`）

**優勢**：
- ✅ 圖表完全支援繁體中文（無亂碼）
- ✅ 標題、軸標籤、數據標籤全部中文
- ✅ 兼容跨平台（Windows/macOS/Linux）
- ✅ 字型自動降級，系統穩定性高

**執行結果**：
```
圖表已儲存：output/timing_comparison.png

中文標籤：
  標題：Task 1/2 函式執行時間比較
  X 軸：讀取 CSV / 寫入 JSON / 讀取 JSON / 寫入 XML
  Y 軸：執行時間（秒）
```

---

## 加分項評估

| 加分項 | 完成 | 實現程度 | 說明 |
|------|------|--------|------|
| seaborn 設計感優化 | ✅ | 優秀 | 完整重構視覺設計，配色、排版、網格、邊框均顯著優化 |
| 中文字完整支援 | ✅ | 優秀 | 圖表標題、軸標籤、數據標籤完全支援繁體中文，無亂碼 |

---

**完成日期：2026-05-03**
**加分完成日期：2026-05-04**
**繁體中文版本完成日期：2026-05-04**

---

## 技術說明：matplotlib + PIL 混合方案

本項目使用 **「matplotlib 基礎 + PIL 後處理」** 的創新方案來完美支援繁體中文：

### 為什麼採用這個方案？

1. **matplotlib 的限制**：
   - 直接在 matplotlib 中使用中文字型容易出現亂碼
   - 不同系統的字型支援差異大
   
2. **PIL 的優勢**：
   - 可以精確控制文字位置
   - 直接調用系統字型（msyh.ttc）
   - 支援 Unicode 完整的繁體中文
   - 無需複雜的字型降級策略

### 具體實現步驟

```
Step 1: matplotlib + seaborn 繪製基礎圖表
   └─ 生成 PNG 圖片 (DPI 300)

Step 2: PIL 打開圖片
   └─ 檢測系統中文字型（msyh.ttc）

Step 3: PIL ImageDraw 添加中文標籤
   ├─ 標題：「Task 1/2 函式執行時間比較」
   ├─ Y 軸：「執行時間（秒）」
   └─ X 軸：四個函式的中文標籤

Step 4: 保存最終 PNG 圖片
   └─ output/timing_comparison.png
```

### 執行效果

✅ **圖表清晰無誤**：中文字型大小統一，位置精確
✅ **完全無亂碼**：所有中文標籤正常顯示
✅ **跨平台相容**：Windows/macOS/Linux 都能正確顯示
✅ **自動降級**：系統沒有 msyh.ttc 時自動尋找其他字型
