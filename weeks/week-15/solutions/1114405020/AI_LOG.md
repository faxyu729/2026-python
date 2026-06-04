## 我問 AI 什麼

請幫我用 unittest 寫 count_squares(a, b) 的測試，至少 3 個案例（含 1 個 edge case + 1 個例外案例）。

## AI 給了什麼

給了 5 個測試：基本案例 (1,10)、edge case 單點平方 (4,4)、單點非平方 (2,2)、負數區間 (-5,5)、和例外案例 (5,2) 應 raise ValueError。

## 我改了什麼

發現 AI 一開始的實作沒處理 a < 0 的情況（math.sqrt 會報錯），我要求修正 square_counter.py 用 max(a, 0) 來處理負數下限，並確認 5 個測試全部通過。
