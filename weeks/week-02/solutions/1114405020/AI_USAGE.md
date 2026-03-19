# AI 輔助使用說明 (AI_USAGE.md)

## 詢問 AI 的問題 (Questions Asked to AI)
1. 如何在 Python 中使用 `unittest` 模組建立多個測試案例的架構？
2. 在 Python 中，如何在不單獨依賴 `set` 的情況下實作去重，並保留原本的順序？
3. 如何在 Python 中使用多個條件對清單進行排序？
4. 如何在 Python 中使用 `Counter` 和 `defaultdict` 進行計數？

## 採納 AI 的建議 (Suggestions Adopted from AI)
- 使用 `unittest.TestCase` 來組織與管理測試方法。
- 在 Task 2 中，採納了使用 `sorted()` 的 `key` 參數搭配 Lambda 函式進行多條件排序的寫法。
- 在 Task 3 中，採納了使用 `collections.Counter` 計算操作次數的建議，快速找出最常出現的操作。
- 採納了將較長程式碼重構為小型輔助函式的建議，以提升可讀性與模組化。

## 拒絕 AI 的建議 (Suggestions Rejected from AI)
- 拒絕了在 Task 1 中單純使用 `set()` 轉換去重的建議，因為題目要求必須保留原先元素出現的順序，而 `set()` 會破壞順序，所以改用輔助的 `set` 搭配迴圈來實作。
- 拒絕了在 Task 2 中手寫排序演算法迴圈的建議，選擇符合題目預期的內建 `sorted()` 函式。

## AI 誤導與自我修正的案例 (Case of AI Misleading and Self-Correction)
- AI 最初建議的排序 `key` 沒有正確處理同分、同年齡時姓名的排序邏輯（AI 提供的是全部降冪）。
- **自我修正**：我修正了排序的 `key`，確保回傳的 Tuple 中姓名的部分為預設（升冪）排列，例如成績同為 85 時，'bob' 應排在 'ian' 前面，藉此與範例輸出完全一致。
