# AI_USAGE.md - AI 使用紀錄

## 1. 我問了哪些問題

1. **CSV 檔案編碼問題**
   - 問題：作業提到 UTF-8-BOM 編碼，應該如何在 Python 中正確讀取？
   - AI 建議：使用 `encoding='utf-8-sig'` 參數
   - 採用情況：✅ 已採用

2. **XML 中文字元處理**
   - 問題：使用 ElementTree 時中文字元如何不出現亂碼？
   - AI 建議：使用 `xml_declaration=True` 和 `encoding='utf-8'` 參數
   - 採用情況：✅ 已採用

3. **裝飾器實作細節**
   - 問題：@timeit 裝飾器如何正確保留原函式的 `__name__` 和 `__doc__`？
   - AI 建議：使用 `functools.wraps` 裝飾器包裝 wrapper 函式
   - 採用情況：✅ 已採用

4. **字典安全存取**
   - 問題：CSV 資料行可能缺少某些欄位，應該如何避免 KeyError？
   - AI 建議：使用 `.get()` 方法搭配預設值
   - 採用情況：✅ 已採用

5. **單元測試的邊界情況**
   - 問題：應該測試哪些邊界情況和反例以確保程式穩健？
   - AI 建議：測試空輸入、缺失值、特殊字元等情況
   - 採用情況：✅ 已採用

---

## 2. AI 建議我有採用的部分

### ✅ 已採用的建議

#### 建議 1：使用 `encoding='utf-8-sig'` 讀取 CSV
```python
# AI 建議的方案
with open(filepath, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
# 我的實作
@timeit
def read_csv(filepath: str) -> list[dict]:
    rows = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows
```

**結果**：成功讀取含 BOM 的 CSV 檔案，未出現編碼問題 ✓

#### 建議 2：使用 `functools.wraps` 保留函式元訊息
```python
# AI 建議的實作
import functools

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # ... 計時邏輯 ...
        return result
    return wrapper
```

**結果**：裝飾後的函式保留原名稱和文件字串，可正常導入和使用 ✓

#### 建議 3：使用 `.get()` 進行安全的字典存取
```python
# 危險的做法
return [r for r in rows if r["入學方式"] == method]  # 會拋出 KeyError

# AI 建議的安全做法
return [r for r in rows if r.get("入學方式") == method]

# 我的實作
def filter_by_admission(rows: list[dict], method: str) -> list[dict]:
    return [r for r in rows if r.get("入學方式") == method]
```

**結果**：即使缺少欄位也能安全執行，測試通過 ✓

#### 建議 4：使用 `collections.Counter` 計算頻次
```python
# AI 建議
from collections import Counter
dept_names = [r.get("系所名稱", "") for r in rows]
return dict(Counter(dept_names))

# 我的實作
def count_by_dept(rows: list[dict]) -> dict:
    if not rows:
        return {}
    dept_names = [r.get("系所名稱", "") for r in rows]
    return dict(Counter(dept_names))
```

**結果**：簡潔高效的系所統計實作 ✓

#### 建議 5：XML 元素建構使用 `ET.SubElement()`
```python
# AI 建議
root = ET.Element("students")
for student in students:
    student_elem = ET.SubElement(root, "student")
    student_elem.set("id", student.get("學號", ""))

# 我的實作
def build_xml_tree(data: dict) -> ET.Element:
    root = ET.Element("students")
    root.set("source", data.get("來源", ""))
    root.set("total", str(data.get("總人數", 0)))
    
    students = data.get("學生清單", [])
    for student in students:
        student_elem = ET.SubElement(root, "student")
        student_elem.set("id", student.get("學號", ""))
        # ...
```

**結果**：正確建構 XML 樹結構 ✓

---

## 3. AI 建議我拒絕的部分及原因

### ❌ 拒絕的建議

#### 拒絕 1：直接從課堂程式複製 @timeit 裝飾器

**AI 建議**：「可以直接從 Week 09 U01 的課堂範例複製 @timeit 裝飾器」

**我的拒絕理由**：
- 作業明確要求「不可直接從課堂範例複製，需自行在各自的檔案中重新實作」
- 盲目複製會失去自己實作的學習價值
- 需要理解裝飾器原理而不是依賴複製

**實際做法**：
自行重新實作，確保理解每一行程式碼的含義

```python
def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timeit] {func.__name__} 耗時 {elapsed:.6f}s")
        return result
    return wrapper
```

#### 拒絕 2：使用 pandas 處理 CSV

**AI 建議**：「使用 pandas.read_csv() 會更簡潔」

**我的拒絕理由**：
- 作業要求學習標準庫（csv、json、xml）
- pandas 是額外依賴，可能不在環境中
- 目的是理解基層 CSV 處理邏輯，而非追求最快實作

**實際做法**：
堅持使用標準庫 csv 模組，確保跨平台相容性

#### 拒絕 3：使用 lxml 庫加速 XML 操作

**AI 建議**：「使用 lxml 的 etree 會比標準 ElementTree 快 2-3 倍」

**我的拒絕理由**：
- 作業題目指定使用 xml.etree.ElementTree
- 本作業重點不在優化效能，而在掌握基礎 API
- 額外依賴增加複雜度，不符合簡潔原則

**實際做法**：
堅持使用標準庫 xml.etree.ElementTree

#### 拒絕 4：省略空值檢查

**AI 建議**：「可以假設資料總是完整的，不需要處理缺失欄位」

**我的拒絕理由**：
- 測試要求包含邊界情況（空輸入、缺失值）
- 實務資料經常不完整
- 省略檢查會導致程式在生產環境中崩潰

**實際做法**：
完整實作邊界情況處理，包括 8+ 個邊界測試

---

## 4. AI 輸出我執行後發現有誤的案例與修正過程

### 案例 1：XML 中文字元亂碼

**AI 初始建議**：
```python
xml_str = ET.tostring(root, encoding='unicode')
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(xml_str)
```

**執行結果**：
❌ 缺少 XML 宣告 `<?xml version="1.0" encoding="utf-8"?>`，部分解析器可能無法正確識別

**修正過程**：
1. 查閱 ElementTree 官方文件
2. 改用 `ET.ElementTree.write()` 方法
3. 添加 `xml_declaration=True` 參數

**修正後的程式**：
```python
@timeit
def write_xml(data: dict, filepath: str) -> None:
    root = build_xml_tree(data)
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)
    # ✓ 現在正確輸出 XML 宣告
```

**驗證**：測試 `test_xml_is_valid` 通過 ✓

---

### 案例 2：Counter 返回型別問題

**AI 初始建議**：
```python
from collections import Counter
return Counter(dept_names)  # 直接返回 Counter 對象
```

**執行結果**：
⚠️ 返回型別是 `Counter` 而不是 `dict`，雖然可以當 dict 使用，但不符合函式簽名要求

**修正過程**：
1. 發現測試中直接比較 `result == dict` 會失敗
2. 意識到需要轉換為純 dict
3. 使用 `dict(Counter(...))` 轉換

**修正後的程式**：
```python
def count_by_dept(rows: list[dict]) -> dict:
    if not rows:
        return {}
    dept_names = [r.get("系所名稱", "") for r in rows]
    return dict(Counter(dept_names))  # ✓ 返回純 dict
```

**驗證**：所有計數測試通過 ✓

---

### 案例 3：時間精度問題

**AI 初始建議**：
```python
print(f"[timeit] {func.__name__} 耗時 {elapsed}s")  # 無精度控制
```

**執行結果**：
⚠️ 耗時可能顯示為 `0.0023419999999999s`（過長且難以讀取）

**修正過程**：
1. 發現對比作業要求的格式 `0.002341s`
2. 添加格式化控制 `.6f`

**修正後的程式**：
```python
print(f"[timeit] {func.__name__} 耗時 {elapsed:.6f}s")
# ✓ 輸出格式: [timeit] read_csv 耗時 0.002341s
```

**驗證**：格式符合作業要求 ✓

---

### 案例 4：JSON 中文顯示

**AI 初始建議**：
```python
json.dump(data, f, indent=2)  # 默認 ensure_ascii=True
```

**執行結果**：
⚠️ JSON 檔案中文字被轉換為 `\u4e2d\u6587` 形式（ASCII escape），雖然功能正常但難以閱讀

**修正過程**：
1. 檢查 JSON 輸出檔案
2. 發現作業要求「學生清單」應該能直接看到中文
3. 添加 `ensure_ascii=False` 參數

**修正後的程式**：
```python
@timeit
def write_json(data: dict, filepath: str) -> None:
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        # ✓ 現在 JSON 檔案可直接讀取中文
```

**驗證**：手動檢查 output/students.json，中文正常顯示 ✓

---

## 5. 總體評估

### AI 幫助程度

| 方面 | 幫助度 | 說明 |
|------|-------|------|
| API 用法理解 | ⭐⭐⭐⭐⭐ | 快速解決編碼和格式化問題 |
| 測試設計 | ⭐⭐⭐⭐ | 提供邊界情況的想法 |
| 除錯 | ⭐⭐⭐ | 幫助診斷但需要手動驗證 |
| 最佳實踐 | ⭐⭐⭐⭐ | .get() 等安全存取方式 |
| 程式結構 | ⭐⭐⭐ | 基本建議合理但需自己調整 |

### 主要收穫

1. **AI 是助手而非替代品**：不應盲目相信，需要自己驗證
2. **理解比複製更重要**：自己實作裝飾器比複製更有價值
3. **標準庫已足夠**：不必追求最新或最快，穩定性優先
4. **文件是最好的老師**：遇到問題查官方文件比問 AI 更靠譜

---

**AI 使用總結**：適度依賴 AI，但保持批判性思維，最終的驗證和決策應由人類承擔。

