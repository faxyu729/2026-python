# 6/11 (四)｜分階段專題：排序效能實驗室

> 把 Week 10 的 `@timeit` 裝飾器、Week 13 的視覺化、Week 14-15 的 TDD + PR 流程,
> 整合成一個完整的小專題。**每個階段都要先紅燈再綠燈,commit 順序就是你的開發證據。**

## 學習目標

- 用 TDD 開發一個可被測試的 `@timeit` 計時裝飾器
- 實作 bubble / quick / merge 三種排序,並用自己的裝飾器量測效能
- 設計至少一種加速方案(Cython 化或演算法優化),用數據證明有效
- 把實驗結果畫成圖,寫出可信的效能報告

---

## 專題總覽(四個階段)

| 階段 | 產出 | 紅燈 commit | 綠燈 commit |
|------|------|------------|------------|
| 1 | `timing.py` — `@timeit` 裝飾器 | `test: stage1 timeit 裝飾器測試` | `feat: stage1 實作 timeit 裝飾器` |
| 2 | `sorts.py` + `benchmark.py` — 三種排序與量測 | `test: stage2 排序正確性測試` | `feat: stage2 實作三種排序與 benchmark` |
| 3 | 加速版排序(Cython 或演算法優化) | `test: stage3 加速版共用正確性測試` | `feat: stage3 加速版與量測數據` |
| 4 | `plot.py` + `assets/benchmark.png` | `test: stage4 繪圖輸出測試` | `feat: stage4 實驗結果圖表與報告` |

`git log --reverse` 必須能看到 **test → feat 交替出現八次**(可穿插 `refactor:`)。
任何一個階段「一開始就綠」或「先 feat 後 test」,該階段流程分 0 分。

---

## Stage 1｜`@timeit` 裝飾器(課堂 0:00–0:25)

寫 `timing.py`,提供裝飾器 `timeit`,規格:

- 被裝飾函式的**回傳值不變**
- 用 `functools.wraps` 保留 `__name__` / `__doc__`
- 每次呼叫後,把耗時(秒,`float`)記錄在:
  - `f.last_elapsed` — 最近一次的耗時
  - `f.records` — 歷次耗時的 list(累積)
- 裝飾器內**不准 `print`**——輸出格式化是 benchmark 的事,計時器保持安靜才能被重複利用

**必備 test case(≥3)**:規格的每一條都要有測試覆蓋。AI 給的測試齊不齊,自己驗收。

## Stage 2｜三種排序 + 量測(課堂 0:25–1:10)

寫 `sorts.py`,三個函式簽名固定:

```python
def bubble_sort(data: list) -> list: ...
def quick_sort(data: list) -> list: ...
def merge_sort(data: list) -> list: ...
```

- 一律**回傳新的 list,不可修改傳入的 list**(測試會驗)
- **禁用** `sorted()` / `list.sort()`——那是 Stage 3 的對照組

**必備 test case(每個函式都要過)**:一般案例之外,edge case 自己想(空的?重複?已排好?),
「不可修改傳入 list」也要有測試。三個函式共用同一組測試——用迴圈 + `subTest`,不要複製貼上三份。

接著寫 `benchmark.py`:

```python
def make_data(n: int, seed: int = 42) -> list: ...   # 固定 seed,實驗可重現
def run_benchmark(sizes=(500, 1000, 2000, 4000), repeats=3) -> dict: ...
```

- 用你自己的 `@timeit` 量測,每個 n 重複 `repeats` 次取 `records` 平均
- `python benchmark.py` 印出比較表,並把結果存成 `results.json`(Stage 4 的輸入)

## Stage 3｜加速實驗(課後)

1. **必做**:把內建 `sorted()`(Timsort,C 實作)加入 benchmark 當 baseline
2. **至少一種加速方案**,自選:
   - **Cython 化**:把任一排序改寫成 `sorts_fast.pyx`(加上 `cdef` 型別註記),
     用 `pip install cython` + `setup.py build_ext --inplace` 或 `pyximport` 編譯
   - **演算法優化**:bubble 提前停止、quick 改 median-of-three、小區間切換插入排序等
3. 加速版**必須通過 Stage 2 同一組正確性測試**(把被測函式做成參數,別再寫一份測試)
4. 加速前後的數據都要進 `results.json`,報告要寫出加速比(例:`bubble 4000 筆:2.31s → 0.18s,12.8x`)

> ⚠️ Cython 編譯產物 `build/`、`*.c`、`*.so` **不准 commit**——只交 `.pyx` 原始碼與編譯指令說明。

## Stage 4｜畫圖與報告(課後)

寫 `plot.py`:

```python
def load_results(path: str) -> dict: ...
def plot_results(results: dict, out_path: str) -> None: ...
```

- 折線圖:x 軸 = 資料量 n,y 軸 = 平均秒數(**y 軸用 log scale**,不然 O(n²) 會把其他線壓扁)
- 每個演算法一條線(含 baseline 與加速版),輸出 `assets/benchmark.png`
- 測試需驗證 PNG 確實產生且非空檔;環境限制:`plot.py` 開頭加 `matplotlib.use("Agg")` 才能在無視窗環境跑
- 在你的 `README.md` 貼圖並用 2–3 句解讀:誰最快?O(n²) 和 O(n log n) 的線斜率差在哪?加速比多少?

---

## 時程與繳交

| 時間 | 內容 |
|------|------|
| 6/11 課堂(90 分鐘) | Stage 1、2 完成並 push;**下課前開出 PR**(之後同分支繼續 push) |
| 課後 | Stage 3、4 |
| **6/17(三)前** | PR 補完全部四階段,完成最終版 |

- 分支:`feature/wk16-0611-<學號>`,PR 標題 `Week 16 - <學號> - <姓名>`
- 所有檔案只能放在 `weeks/week-16/solutions/<學號>/0611/`(CI 會檢查)

### 繳交內容清單

```
weeks/week-16/solutions/<學號>/0611/
├── timing.py  test_timing.py
├── sorts.py   test_sorts.py
├── benchmark.py  results.json
├── sorts_fast.pyx(或演算法優化版)
├── plot.py    test_plot.py
├── assets/benchmark.png
├── README.md      # 實驗報告:方法、數據表、圖、解讀、加速比
├── AI_LOG.md      # 提示詞逐字記錄(規則同 6/10)
└── TEST_LOG.md    # 每階段至少一紅一綠的 unittest 輸出
```

### 評分(納入作業成績)

| 項目 | 配分 |
|------|------|
| Stage 1 timeit 正確 + 測試完整 | 15 |
| Stage 2 三排序正確 + 共用測試 + benchmark 可重現 | 25 |
| Stage 3 加速有效 + 通過共用測試 + 數據佐證 | 10 |
| Stage 4 圖表正確 + 解讀合理 | 10 |
| Code Style(命名、繁中註解、無重複測試碼) | 20 |
| 報告與紀錄(README / AI_LOG / TEST_LOG / commit 順序) | 20 |

---

## 課末自我檢測(不翻文件回答)

1. `last_elapsed` 為什麼掛在 wrapper 上,不用全域變數?
2. 為什麼測試要驗「原 list 未被修改」?哪個排序最容易不小心改到?
3. benchmark 為什麼要固定 seed、重複多次取平均?
4. 你的加速方案如果只跑 n=500 看不出差異,該怎麼設計實驗?
5. 八個 commit 的順序是什麼?哪一種順序會直接 0 流程分?

---

## AI 使用規則(同 6/10)

提示詞自己打、逐字記入 `AI_LOG.md`;「我改了什麼」0 字 = 期末考此項 0 分。
AI 給的測試齊不齊、排序對不對、圖正不正確——**你自己驗收**,驗收標準寫進 AI_LOG。

## starter 檔

```bash
cp -r weeks/week-16/in_class/0611-sort-starter weeks/week-16/solutions/<學號>/0611
```
