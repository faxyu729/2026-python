# TEST_LOG

## Red（失敗）

- 執行時間：2026-03-12
- 指令：

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- 摘要：
  - 測試總數：2（載入測試模組）
  - 通過：0
  - 失敗：0
  - 錯誤：2
- 主要錯誤：`ModuleNotFoundError: No module named 'robot_core'`
- 說明（從失敗到修正）：
  - 測試先行建立後，因核心邏輯尚未存在導致匯入失敗，符合 Red 階段。

## Green（全通過）

- 執行時間：2026-03-12
- 指令：

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- 摘要：
  - 測試總數：11
  - 通過：11
  - 失敗：0
- 說明（從失敗到通過）：
  - 實作 `robot_core.py` 的旋轉、越界、LOST、scent 規則與非法指令策略，並整理函式切分後測試全綠。

## Refactor 紀錄

- 調整內容：
  - 將 HUD 繪製改成接收 frame 對應的 scent 快照，修正回放資料不一致。
- 結果：
  - 重新執行測試仍為 11/11 通過。
