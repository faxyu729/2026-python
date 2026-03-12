# TEST_CASES

> 說明：以下實際結果以目前程式執行結果填寫。對應測試函式皆可在 `tests/` 找到。

## Case 01：左轉基本規則

- 輸入：`(0,0,N), commands="L"`
- 預期結果：方向變 `W`
- 實際結果：方向 `W`
- PASS/FAIL：PASS
- 對應測試函式：`test_turn_left_from_north_is_west`

## Case 02：右轉基本規則

- 輸入：`(0,0,N), commands="R"`
- 預期結果：方向變 `E`
- 實際結果：方向 `E`
- PASS/FAIL：PASS
- 對應測試函式：`test_turn_right_from_north_is_east`

## Case 03：連續旋轉回原方向

- 輸入：`direction="N"`, 連續 `R` 四次
- 預期結果：回到 `N`
- 實際結果：`N`
- PASS/FAIL：PASS
- 對應測試函式：`test_four_right_turns_back_to_original`

## Case 04：邊界內前進

- 輸入：`(0,0,N), commands="F", map=(5,3)`
- 預期結果：到 `(0,1,N)` 且不 LOST
- 實際結果：`(0,1,N), lost=False`
- PASS/FAIL：PASS
- 對應測試函式：`test_forward_inside_boundary_not_lost`

## Case 05：邊界外掉落

- 輸入：`(5,3,N), commands="F", map=(5,3)`
- 預期結果：停在 `(5,3,N)` 並 LOST，留下 scent
- 實際結果：`(5,3,N), lost=True`，scent 含 `(5,3,'N')`
- PASS/FAIL：PASS
- 對應測試函式：`test_forward_outside_boundary_becomes_lost`、`test_first_robot_leaves_scent_after_lost`

## Case 06：同位置同方向 scent 生效

- 輸入：`scents={(5,3,'N')}`, `(5,3,N), commands="F"`
- 預期結果：忽略該步，不 LOST
- 實際結果：位置不變 `(5,3,N)`, `lost=False`
- PASS/FAIL：PASS
- 對應測試函式：`test_second_robot_ignores_dangerous_forward_on_same_scent`

## Case 07：同格不同方向不可共用 scent

- 輸入：`scents={(5,3,'N')}`, `(5,3,E), commands="F"`
- 預期結果：仍會越界 LOST
- 實際結果：`lost=True`
- PASS/FAIL：PASS
- 對應測試函式：`test_same_cell_different_direction_should_not_share_scent`

## Case 08：LOST 後仍有後續指令

- 輸入：`(5,3,N), commands="FRF"`
- 預期結果：第一步 `F` 就 LOST，後續不執行
- 實際結果：停在 `(5,3,N), lost=True`
- PASS/FAIL：PASS
- 對應測試函式：`test_lost_robot_stops_processing_remaining_commands`

## Case 09：有 scent 先忽略危險，再執行後續指令

- 輸入：`scents={(5,3,'N')}`, `(5,3,N), commands="FRF"`
- 預期結果：第一個 `F` 被忽略，`R` 後朝東，最後 `F` 越界 LOST
- 實際結果：`(5,3,E), lost=True`
- PASS/FAIL：PASS
- 對應測試函式：`test_ignore_scent_and_continue_following_commands`

## Case 10：非法指令處理

- 輸入：`(0,0,N), commands="FX"`, policy=`raise`
- 預期結果：丟出 `ValueError`
- 實際結果：`ValueError`
- PASS/FAIL：PASS
- 對應測試函式：`test_invalid_command_raises_value_error`
