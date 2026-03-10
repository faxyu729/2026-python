# TEST_CASES.md

## Test Case 1: Normal Input for Task 1
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

**Corresponding Test Function:** tests/test_task1.py::TestSequenceClean::test_normal_case  

**Key Fix Point:** Implemented deduplication without using set directly, preserving order.

## Test Case 2: Edge Case for Task 1 (Empty Input)
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

**Corresponding Test Function:** tests/test_task1.py::TestSequenceClean::test_empty_input  

**Key Fix Point:** Added check for empty input to return empty strings.

## Test Case 3: Anti-Case for Task 1 (No Evens)
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

**Corresponding Test Function:** tests/test_task1.py::TestSequenceClean::test_no_evens  

**Key Fix Point:** Correctly filtered even numbers, returning empty for no evens.

## Test Case 4: Normal Input for Task 2
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

**Corresponding Test Function:** tests/test_task2.py::TestStudentRanking::test_normal_case  

**Key Fix Point:** Used sorted with correct key for multi-level sorting.

## Test Case 5: Tie-Breaking for Task 2
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

**Corresponding Test Function:** tests/test_task2.py::TestStudentRanking::test_tie_breaking  

**Key Fix Point:** Ensured sorting handles ties by age and name correctly.