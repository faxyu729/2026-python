# QUESTION-299 簡化版本測試日誌

## 簡化版本特點

此版本用於競賽中手寫練習：
- 代碼簡潔易寫
- 使用冒泡排序計數交換
- 直接使用len()而非變數l

## 測試環境
- **測試日期**：2026年3月19日
- **Python版本**：3.14
- **測試方法**：與完整版本的輸入輸出對比

## 測試結果

### 測試輸入
```
5
4
2 3 1 4
3
2 4 1 3
2
3 2 1
2
1 2
5
4 3 2 1
```

### 簡化版本輸出
```
Optimal train swapping takes 2 swaps.
Optimal train swapping takes 3 swaps.
Optimal train swapping takes 3 swaps.
Optimal train swapping takes 0 swaps.
Optimal train swapping takes 6 swaps.
```

### 完整版本輸出
```
Optimal train swapping takes 2 swaps.
Optimal train swapping takes 3 swaps.
Optimal train swapping takes 3 swaps.
Optimal train swapping takes 0 swaps.
Optimal train swapping takes 6 swaps.
```

### 對比結果
✅ **完全一致** - 5/5 輸出行匹配

## 手寫複習要點

簡化版本的關鍵：

1. **讀取測資**
   ```python
   n = int(input())
   for _ in range(n):
       l = int(input())
   ```

2. **邊界情況**
   ```python
   if l == 0:
       print("Optimal train swapping takes 0 swaps.")
   ```

3. **冒泡排序計數**
   ```python
   swaps = 0
   for i in range(len(arr)):
       for j in range(len(arr) - 1 - i):
           if arr[j] > arr[j + 1]:
               arr[j], arr[j + 1] = arr[j + 1], arr[j]
               swaps += 1
   ```

4. **輸出格式**
   ```python
   print(f"Optimal train swapping takes {swaps} swaps.")
   ```

## 結論

✅ 簡化版本與完整版本功能完全相同，只有15行核心代碼，易於手寫。
