# 赤壁戰役 - AI 使用說明

## 概述

本作業文件詳細說明了 AI 在協助編寫「赤壁戰役 - 三國戰役模擬系統」時的使用時機與限制。目的是確保學習過程中保持誠實性，同時合理運用 AI 工具提高開發效率。

---

## ✅ 允許使用 AI 的時機

### 1. 不懂如何寫測試時
**場景**：
- 不清楚 unittest 的 setUp/tearDown 用法
- 不知道如何編寫 Arrange-Act-Assert 模式
- 需要理解測試命名慣例

**適當做法**：
```python
# ✓ 可以請 AI 解釋這種模式
class TestExample(unittest.TestCase):
    def setUp(self):
        """每個測試前準備"""
        # Arrange: 準備環境
    
    def test_something(self):
        # Act: 執行動作
        # Assert: 驗證結果
```

### 2. 實現遇到 Python 語法問題時
**場景**：
- `namedtuple` 的正確語法
- `Counter` 的 `most_common()` 方法用法
- `defaultdict` 的初始化方式
- 字典推導式或列表推導式的寫法

**適當做法**：
```python
# ✓ 可以請 AI 檢查語法
from collections import Counter
damage_ranking = counter.most_common(5)

# ✓ 可以請 AI 解釋這段代碼的含義
factions = Counter(g.faction for g in generals.values())
```

### 3. ASCII 視覺化時
**場景**：
- 需要製作進度條 (█ 和 ░)
- 製作表格格式
- 美化輸出

**適當做法**：
```python
# ✓ 可以請 AI 幫助製作視覺效果
bar = '█' * (dmg // 5) + '░' * (20 - dmg // 5)
print(f"  {name:8} {bar} {dmg:3} HP")
```

### 4. 需要重構代碼時
**場景**：
- 代碼冗餘，需要提取共同邏輯
- 需要改進代碼可讀性
- 需要重新組織函數結構

**適當做法**：
```python
# ✓ 可以請 AI 建議重構方案
# 原始代碼有重複，可以提取成函數
def calculate_faction_damage(damage_dict, generals, faction):
    return sum(dmg for name, dmg in damage_dict.items()
               if generals[name].faction == faction)
```

---

## ❌ 禁止使用 AI 的地方

### 1. 完整複製 AI 生成的代碼
**錯誤做法** ❌：
```python
# 直接複製整個 ChibiBattle 類別實現
# 而不理解每一行代碼的含義
class ChibiBattle:
    # ... 複製的代碼 ...
```

**正確做法** ✓：
- 請 AI 解釋如何實現某功能
- 自己動手寫代碼，參考 AI 的建議
- 測試代碼並理解每一行的作用

### 2. 跳過 TDD 三階段流程
**錯誤做法** ❌：
```python
# 只生成代碼，不寫測試
# 或只複製測試，不思考邏輯
```

**正確做法** ✓：
1. **RED 階段**：先寫失敗的測試
2. **GREEN 階段**：用最簡單的方式讓測試通過
3. **REFACTOR 階段**：改進代碼品質

### 3. 使用型別壓制方式 (`as any` 或 `@ts-ignore` 等)
**錯誤做法** ❌：
```python
# Python 中的等價做法（避免）
result = game.get_generals() # type: ignore
```

**正確做法** ✓：
- 理解型別系統
- 正確宣告類型
- 確保代碼類型安全

---

## 推薦作法 (TDD 流程)

### 第 1 步：自己寫測試 (RED)
```python
# ✓ 自己動手寫測試
def test_load_generals_from_file(self):
    """測試 1-1: 正確讀取 9 位武將"""
    game = ChibiBattle()
    game.load_generals('generals.txt')
    self.assertEqual(len(game.generals), 9)
```

### 第 2 步：看測試失敗
```bash
$ python -m pytest test_chibi.py::TestStage1DataLoading::test_load_generals_from_file -v

FAILED - AttributeError: 'ChibiBattle' object has no attribute 'load_generals'
```

### 第 3 步：AI 協助實現 (GREEN)
```python
# ✓ 詢問 AI：「如何在 Python 中讀取檔案和 EOF？」
# AI 回答後，自己編寫代碼：

def load_generals(self, filename):
    """Week 07: 讀取武將資料，EOF 結尾"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == 'EOF':
                break
            # ... 自己完成其他部分 ...
```

### 第 4 步：自己重構 (REFACTOR)
```python
# ✓ 自己改進代碼
# 例如：提取解析邏輯成獨立函數
def parse_general_line(self, line):
    """提取：解析一行武將資料"""
    parts = line.split()
    # ... 實現 ...
    return general
```

### 第 5 步：確認所有測試通過
```bash
$ python -m pytest test_chibi.py -v

============================= 16 passed =============================
✅ 所有測試通過
```

---

## 本作業中的 AI 使用實況

### Stage 1 (資料讀取)
- **使用 AI**：理解檔案 I/O 和 EOF 處理
- **自己寫**：測試案例和具體實現
- **結果**：✓ 4 個測試通過

### Stage 2 (戰鬥模擬)
- **使用 AI**：`sorted()` 的 `key` 參數用法
- **自己寫**：戰鬥邏輯和統計算法
- **結果**：✓ 9 個測試通過

### Stage 3 (視覺化)
- **使用 AI**：ASCII 進度條製作
- **自己寫**：報告格式和輸出邏輯
- **結果**：✓ 3 個測試通過，視覺化清晰

---

## 常見 AI 提問範本

### 詢問語法時
> 「Python 中 `Counter` 的 `most_common()` 方法如何使用？請給出一個例子。」

### 詢問邏輯時
> 「如何使用 `defaultdict` 追蹤多個對象的累計傷害？」

### 詢問重構時
> 「這段代碼有重複的邏輯，應該如何提取成函數？」

### 詢問測試時
> 「在 unittest 中，setUp 和 tearDown 方法如何使用？」

---

## 誠實性檢查清單

在提交作業前，檢查以下項目：

- [ ] 我能逐行解釋 `chibi_battle.py` 中的代碼
- [ ] 我理解為什麼 `Counter` 用於傷害統計，`defaultdict` 用於兵力損失
- [ ] 我能夠解釋三階段 TDD 流程的目的
- [ ] 我知道每個測試案例在驗證什麼
- [ ] 我沒有複製 AI 生成的完整代碼區塊（除了簡短片段）
- [ ] 所有 16 個測試都通過了，且我理解它們的含義

---

## 如果你被卡住了

### 情況 1：不知道如何開始
**建議**：
1. 閱讀 HOMEWORK.md 的 Stage 1
2. 自己寫 4 個測試
3. 看它們全部失敗（RED）
4. 再根據測試需求實現功能

### 情況 2：測試通不過
**建議**：
1. 檢查測試的預期值是否正確
2. 使用 `print()` 調試輸出
3. 逐步追蹤代碼執行

### 情況 3：代碼看起來太複雜
**建議**：
1. 分解成更小的函數
2. 為每個函數編寫單獨的測試
3. 一次只改進一個函數

---

## 最後的話

AI 是一個強大的工具，但**理解勝於速度**。

- ✓ 用 AI 加速學習（理解語法、解釋概念）
- ✗ 不要用 AI 跳過學習（複製整個實現）

記住：
> **你學到的不是代碼本身，而是如何思考和解決問題的能力。**

祝你編碼順利！🚀
