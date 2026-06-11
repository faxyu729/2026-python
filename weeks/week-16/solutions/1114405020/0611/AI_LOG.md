# AI_LOG

## Stage 1 — @timeit 裝飾器

**我問 AI 什麼**：請幫我用 `unittest` 寫 `@timeit` 裝飾器的測試，至少 3 個 case，含 1 個 edge case。

**AI 給了什麼**：給了 6 個測試（回傳值、metadata、計時記錄、例外記錄、無 print、多次累積），以及 stub 和完整實作。

**我改了什麼**：確認檢查表（簽名/例外/edge case）齊全後執行紅燈 commit，接著接受綠燈實作。測試中 `add()` 無參數 case 有 bug（原函式需 2 參數），我自行修正移除該 assertion。

## Stage 2 — 三種排序 + benchmark

**我問 AI 什麼**：請幫我用 `unittest` 寫 bubble/quick/merge sort 的測試，全部用 `subTest` 共用，含所有 edge case 和 input mutation 檢查。

**AI 給了什麼**：給了 8 個測試方法，以及三種排序的實作。

**我改了什麼**：確認所有 edge case 列表後執行紅燈 commit。實作中 quick sort 使用 list comprehension 確保不修改輸入 list。

## Stage 3 — 加速實驗

**我問 AI 什麼**：請幫我寫加速排序的測試，至少 3 個 case，含 edge case；並實作 bubble_sort_fast（early stopping）和 quick_sort_fast（median-of-three）。

**AI 給了什麼**：給了 3 個測試（正確性、input mutation、edge cases）和加速版實作。

**我改了什麼**：確認加速版須通過 Stage 2 相同測試邏輯。benchmark 加入 `builtin_sorted` baseline 與加速版。

## Stage 4 — 畫圖

**我問 AI 什麼**：請寫 `plot.py` 含 `load_results` 和 `plot_results`，y 軸 log scale，輸出 PNG；並寫測試驗證 PNG 非空。

**AI 給了什麼**：給了 4 個測試和 plot 實作。

**我改了什麼**：執行 benchmark.py 產生正式 `results.json` 後執行 `plot.py` 輸出 `assets/benchmark.png`。

## Stage 5 — 安全自掃

**我問 AI 什麼**：根據 OpenSSF Secure Coding Guide 第 3/4/5/8 章，掃描 Stage 1-4 程式，找出 3 條適用問題並寫測試。

**AI 給了什麼**：給了 4 個安全測試和對應的程式修正。

**我改了什麼**：判定 `make_data` 應驗證 n>0、`load_results` 應使用 `with` 關檔、讀檔應使用 `json` 而非 `pickle`（CWE-502）。`random` 用於 benchmark 非安全敏感，不需改 `secrets`，判定不適用。
