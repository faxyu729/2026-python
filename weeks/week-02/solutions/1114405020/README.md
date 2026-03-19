# Week 02 實作摘要 - 1114405020

## 完成的任務 (Completed Tasks)
- Task 1: Sequence Clean (序列清理)
- Task 2: Student Ranking (學生排名)
- Task 3: Log Summary (日誌摘要)

## 執行環境 (Execution Environment)
- 程式語言: Python 3.12.1
- 依賴套件: 無外部套件，僅使用標準函式庫 (unittest, collections)

## 程式執行方式 (Program Execution Instructions)
每個任務都可以獨立執行模組或匯入函式：
- Task 1: `python task1_sequence_clean.py` (註：此為模組，請在程式中呼叫 `sequence_clean` 函式)
- Task 2: `python task2_student_ranking.py` (呼叫 `student_ranking` 函式)
- Task 3: `python task3_log_summary.py` (呼叫 `log_summary` 函式)

## 測試執行方式 (Test Execution Instructions)
請在終端機中執行以下指令來執行所有單元測試：
`python -m unittest discover -s tests -p "test_*.py" -v`

## 資料結構選擇 (Data Structure Choices)
- **Task 1:** 使用 `list` 和 `set` 進行去重，以保持順序同時不違反時間複雜度限制；使用字串進行輸出格式化。
- **Task 2:** 使用 `list of tuples` 來儲存學生資料，並利用帶有 `key` 的 `sorted()` 進行高效的多條件排序。
- **Task 3:** 使用 `defaultdict` 計算使用者的動作次數，並使用 `Counter` 計算不同動作的總次數，可有效處理動態計算。

## 遭遇的錯誤與解決方式 (One Error Encountered and Fix)
在 Task 2 中，最初誤解了姓名相同時的排序規則；後來透過修正 `sorted` 的 `key`（確保成績、年齡相同時，姓名依升冪排序）成功解決。

## Red → Green → Refactor 流程總結

### Task 1: Sequence Clean
- **Red:** 撰寫了正常情況、空字串及無偶數情況的測試，由於尚未實作，測試全部失敗。
- **Green:** 實作 `sequence_clean` 函式，包含去重迴圈、排序與偶數過濾，使測試通過。
- **Refactor:** 將程式碼拆分為輔助函式 (`remove_duplicates_preserve_order`, `get_even_numbers`)，提升模組化與可讀性。

### Task 2: Student Ranking
- **Red:** 建立正常排名、k=0 及同分情況的測試，因函式未定義而失敗。
- **Green:** 新增 `student_ranking` 函式，包含輸入解析與使用正確的 key 進行 `sorted()`，修復預期輸出後測試通過。
- **Refactor:** 拆分為 `parse_input`、`sort_students` 與 `format_output` 函式，落實關注點分離。

### Task 3: Log Summary
- **Red:** 定義正常日誌、空日誌與相同動作的測試，因缺少函式發生 import error。
- **Green:** 使用 `defaultdict` 和 `Counter` 實作 `log_summary`；處理如 m=0 的邊界情況。
- **Refactor:** 將程式碼分為 `parse_logs`、`get_sorted_user_counts` 與 `get_top_action`，讓結構更簡潔。
