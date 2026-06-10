# AI_LOG

## 我問 AI 什麼

> 逐字提示詞（依序）：

1. `讀{C:\Users\linyo\python\0610\2026-python\weeks\week-16\in_class\0610-starter\README.md}拆解≥3 個 test case`

2. `幫我寫{C:\Users\linyo\python\0610\2026-python\weeks\week-16\in_class\0610-starter\test_digit_root.py}→ 紅燈 → test: commit並放入{C:\Users\linyo\python\0610\2026-python\weeks\week-16\solutions\1114405020}中`

3. `幫我寫測試digit_root.py → 綠燈 → feat: commit並放入{C:\Users\linyo\python\0610\2026-python\weeks\week-16\solutions\1114405020\0610}中`

## AI 給了什麼

1. 拆出 3 類 test case：基本案例（24/199/9999）、edge case（一位數/大數）、例外案例（0/-1/-100），並給出合併後的 test code。
2. 寫入 `test_digit_root.py`、執行確認紅燈、複製到 solutions、以 `test:` commit。
3. 寫入 `digit_root.py`（while 迴圈實作 digit root 邏輯）、執行確認全綠、複製到 solutions、以 `feat:` commit。

## 我改了什麼

檢查了測試涵蓋範圍：basic 案例涵蓋多位數正常流程、edge case 包含一位數與大數邊界、invalid input 涵蓋 0 與負數，符合題目「至少 1 個 edge case + 1 個例外案例」要求。digit_root.py 的 Exception message 一字不差對過 spec 的 `"n must be >= 1"`。測試從 ImportError 紅燈到 3/3 全綠無誤後才 commit。
