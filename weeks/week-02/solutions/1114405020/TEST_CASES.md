# 測試案例文件 (TEST_CASES.md)

## Test Case 1: Task 1 正常輸入情況 (Normal Input for Task 1)
**Input:**  
"5 3 5 2 9 2 8 3 1"

**Expected Output:**  
dedupe: 5 3 2 9 8 1  
asc: 1 2 2 3 3 5 5 8 9  
desc: 9 8 5 5 3 3 2 2 1  
evens: 2 2 8  

**Actual Output:**  
dedupe: 5 3 2 9 8 1  
asc: 1 2 2 3 3 5 5 8 9  
desc: 9 8 5 5 3 3 2 2 1  
evens: 2 2 8  

**Pass/Fail:** PASS  

**對應的測試函式 (Corresponding Test Function):** `tests/test_task1.py::TestSequenceClean::test_normal_case`  

**修復重點 (Key Fix Point):** 在不直接將結果轉為 set 的情況下實作了去重功能，成功保留了原本的順序。

## Test Case 2: Task 1 邊界情況 - 空輸入 (Edge Case for Task 1: Empty Input)
**Input:**  
""

**Expected Output:**  
dedupe: ""  
asc: ""  
desc: ""  
evens: ""  

**Actual Output:**  
dedupe: ""  
asc: ""  
desc: ""  
evens: ""  

**Pass/Fail:** PASS  

**對應的測試函式 (Corresponding Test Function):** `tests/test_task1.py::TestSequenceClean::test_empty_input`  

**修復重點 (Key Fix Point):** 新增了空字串的檢查，確保輸入為空時回傳空字串。

## Test Case 3: Task 1 反向情況 - 無偶數 (Anti-Case for Task 1: No Evens)
**Input:**  
"1 3 5 7 9"

**Expected Output:**  
dedupe: 1 3 5 7 9  
asc: 1 3 5 7 9  
desc: 9 7 5 3 1  
evens: ""  

**Actual Output:**  
dedupe: 1 3 5 7 9  
asc: 1 3 5 7 9  
desc: 9 7 5 3 1  
evens: ""  

**Pass/Fail:** PASS  

**對應的測試函式 (Corresponding Test Function):** `tests/test_task1.py::TestSequenceClean::test_no_evens`  

**修復重點 (Key Fix Point):** 正確過濾偶數；如果沒有偶數則回傳空字串。

## Test Case 4: Task 2 正常輸入情況 (Normal Input for Task 2)
**Input:**  
6 3  
amy 88 20  
bob 88 19  
zoe 92 21  
ian 88 19  
leo 75 20  
eva 92 20  

**Expected Output:**  
eva 92 20  
zoe 92 21  
bob 88 19  

**Actual Output:**  
eva 92 20  
zoe 92 21  
bob 88 19  

**Pass/Fail:** PASS  

**對應的測試函式 (Corresponding Test Function):** `tests/test_task2.py::TestStudentRanking::test_normal_case`  

**修復重點 (Key Fix Point):** 正確使用 `sorted()` 函式搭配 `key` 參數進行多條件排序。

## Test Case 5: Task 2 同分情況處理 (Tie-Breaking for Task 2)
**Input:**  
4 4  
bob 88 19  
ian 88 19  
amy 88 20  
zoe 88 21  

**Expected Output:**  
bob 88 19  
ian 88 19  
amy 88 20  
zoe 88 21  

**Actual Output:**  
bob 88 19  
ian 88 19  
amy 88 20  
zoe 88 21  

**Pass/Fail:** PASS  

**對應的測試函式 (Corresponding Test Function):** `tests/test_task2.py::TestStudentRanking::test_tie_breaking`  

**修復重點 (Key Fix Point):** 確保排序邏輯在處理同分數、同年齡的學生時，能正確依姓名進行排序。
