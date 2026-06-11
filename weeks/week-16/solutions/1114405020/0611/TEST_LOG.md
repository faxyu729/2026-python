# TEST_LOG

## Stage 1 — @timeit 裝飾器

### 紅燈 (test: stage1 timeit 裝飾器測試)

```
$ python -m unittest test_timing -v
test_no_print ... FAIL
test_preserves_function_metadata ... FAIL
test_records_elapsed_time ... ERROR
test_records_multiple_calls_accumulate ... ERROR
test_records_on_exception ... ERROR
test_returns_original_result ... ERROR

Ran 6 tests in 0.008s
FAILED (failures=2, errors=4)
```

### 綠燈 (feat: stage1 實作 timeit 裝飾器)

```
$ python -m unittest test_timing -v
test_no_print ... ok
test_preserves_function_metadata ... ok
test_records_elapsed_time ... ok
test_records_multiple_calls_accumulate ... ok
test_records_on_exception ... ok
test_returns_original_result ... ok

Ran 6 tests in 0.001s
OK
```

## Stage 2 — 排序正確性測試

### 紅燈 (test: stage2 排序正確性測試)

```
$ python -m unittest test_sorts -v
test_all_identical ... FAIL (×3)
test_already_sorted ... FAIL (×3)
test_empty ... ok
test_input_not_mutated ... ok
test_random_data_matches_builtin ... FAIL (×3)
test_reverse_sorted ... FAIL (×3)
test_single_element ... FAIL (×3)
test_with_duplicates ... FAIL (×3)

Ran 8 tests in 0.013s
FAILED (failures=18)
```

### 綠燈 (feat: stage2 實作三種排序與 benchmark)

```
$ python -m unittest test_sorts -v
test_all_identical ... ok
test_already_sorted ... ok
test_empty ... ok
test_input_not_mutated ... ok
test_random_data_matches_builtin ... ok
test_reverse_sorted ... ok
test_single_element ... ok
test_with_duplicates ... ok

Ran 8 tests in 0.007s
OK
```

## Stage 3 — 加速版

### 紅燈 (test: stage3 加速版共用正確性測試)

```
$ python -m unittest test_sorts_fast -v
test_correctness ... FAIL (×2)
test_edge_cases ... FAIL (×8)
test_input_not_mutated ... ok

Ran 3 tests in 0.006s
FAILED (failures=10)
```

### 綠燈 (feat: stage3 加速版與量測數據)

```
$ python -m unittest test_sorts_fast -v
test_correctness ... ok
test_edge_cases ... ok
test_input_not_mutated ... ok

Ran 3 tests in 0.000s
OK
```

## Stage 4 — 繪圖

### 紅燈 (test: stage4 繪圖輸出測試)

```
$ python -m unittest test_plot -v
test_load_results_file_not_found ... FAIL
test_load_results_invalid_json ... FAIL
test_load_results_valid ... FAIL
test_plot_creates_nonempty_png ... FAIL

Ran 4 tests in 0.006s
FAILED (failures=4)
```

### 綠燈 (feat: stage4 實驗結果圖表與報告)

```
$ python -m unittest test_plot -v
test_load_results_file_not_found ... ok
test_load_results_invalid_json ... ok
test_load_results_valid ... ok
test_plot_creates_nonempty_png ... ok

Ran 4 tests in 2.760s
OK
```

## Stage 5 — 安全性

### 紅燈 (test: stage5 安全性規則測試)

```
$ python -m unittest test_security -v
test_load_uses_json_not_pickle ... ERROR
test_make_data_rejects_negative ... FAIL
test_make_data_rejects_zero ... FAIL
test_results_file_closed ... ERROR

Ran 4 tests in 0.006s
FAILED (failures=2, errors=6)
```

### 綠燈 (feat: stage5 修正安全性問題)

```
$ python -m unittest test_security -v
test_load_uses_json_not_pickle ... ok
test_make_data_rejects_negative ... ok
test_make_data_rejects_zero ... ok
test_results_file_closed ... ok

Ran 4 tests in 0.006s
OK
```

## 全測試總覽

```
$ python -m unittest discover -v

test_load_results_file_not_found ... ok
test_load_results_invalid_json ... ok
test_load_results_valid ... ok
test_plot_creates_nonempty_png ... ok
test_load_uses_json_not_pickle ... ok
test_make_data_rejects_negative ... ok
test_make_data_rejects_zero ... ok
test_results_file_closed ... ok
test_all_identical ... ok
test_already_sorted ... ok
test_empty ... ok
test_input_not_mutated ... ok
test_random_data_matches_builtin ... ok
test_reverse_sorted ... ok
test_single_element ... ok
test_with_duplicates ... ok
test_correctness ... ok
test_edge_cases ... ok
test_input_not_mutated ... ok
test_no_print ... ok
test_preserves_function_metadata ... ok
test_records_elapsed_time ... ok
test_records_multiple_calls_accumulate ... ok
test_records_on_exception ... ok
test_returns_original_result ... ok

Ran 25 tests in 0.416s
OK
```
