# U04. 數字精度的陷阱與選擇（3.1–3.7）
# 本程式展示數字處理的常見陷阱：
# 1. 銀行家捨入 / 2. NaN 無法比較 / 3. float vs Decimal 的選擇

import math
import timeit
from decimal import Decimal, ROUND_HALF_UP

# ── 銀行家捨入（3.1）─────────────────────────────────
# 問題：Python round() 使用「四捨六入五取偶」(banker's rounding)
#      不是日常生活中的「四捨五入」，容易產生意外結果
# 原理：當尾數恰好是 5 時，會四捨五入到最近的「偶數」

print(round(0.5))  # 0（不是 1！）0.5 → 0（0 是偶數）
print(round(2.5))  # 2（不是 3！）2.5 → 2（2 是偶數）
print(round(3.5))  # 4（3.5 → 4，4 是偶數）
#
# 說明：
#   - round(0.5) 預期是 1，但結果是 0
#   - round(2.5) 預期是 3，但結果是 2
#   - 這是 IEEE 754 浮點數標準定義的行為
#   - 設計目的：在大量統計中避免系統性的捨入誤差


# ✓ 若需傳統四捨五入，用 Decimal + ROUND_HALF_UP
def trad_round(x: float, n: int = 0) -> Decimal:
    # x：要捨入的浮點數
    # n：小數位數（預設 0 位 = 整數）

    d = Decimal(str(x))  # 將浮點數轉換為 Decimal
    # 重要：先轉 str 再轉 Decimal，避免浮點誤差傳入

    if n == 0:
        fmt = Decimal("1")  # 捨入到整數
    else:
        fmt = Decimal("0." + "0" * n)  # 捨入到 n 位小數
    # 例如 n=2 時，fmt = Decimal("0.00")

    return d.quantize(fmt, rounding=ROUND_HALF_UP)
    # quantize()：將 d 捨入到 fmt 指定的精度
    # ROUND_HALF_UP：標準的四捨五入（≥5 捨入）


print(trad_round(0.5))  # 1（正確！）
print(trad_round(2.5))  # 3（正確！）

# ── NaN 無法用 == 比較（3.7）─────────────────────────
# 問題：NaN (Not a Number) 是特殊的浮點數值，違反了數學上的相等性
#      NaN != NaN，使用 == 進行比較會永遠傳回 False
# 原理：IEEE 754 標準規定 NaN 與任何值（包括自己）都不相等

c = float("nan")  # 建立 NaN 值

# ❌ 錯誤的比較方式
print(c == c)  # False（自己不等於自己！這違反直覺）
print(c == float("nan"))  # False（兩個 NaN 也不相等）

# ✓ 正確的檢測方式：使用 math.isnan()
print(math.isnan(c))  # True（唯一正確的檢測 NaN 的方法）

# 實例：從數據中清除 NaN 值
data = [1.0, float("nan"), 3.0, float("nan"), 5.0]
clean = [x for x in data if not math.isnan(x)]
# 列表推導式逐項檢查，使用 math.isnan() 判斷是否為 NaN
print(clean)  # [1.0, 3.0, 5.0]
#
# 說明：
#   - data 中包含兩個 NaN 值
#   - 篩選出所有非 NaN 的值
#   - 結果只保留了 1.0, 3.0, 5.0

# ── float vs Decimal 選擇（3.2）──────────────────────
# 問題：float 使用二進位浮點數，無法精確表示某些十進位小數
#      導致累積誤差，特別是在金融計算中不可接受
# Decimal 使用十進位，精確但效能較差

print("\n[float 的問題]")
print(0.1 + 0.2)  # 0.30000000000000004（不是 0.3！）
# 原因：0.1 和 0.2 在二進位浮點中無法精確表示
# 0.1 ≈ 0.1000000000000000055511151231257827...
# 0.2 ≈ 0.2000000000000000111022302462515654...
# 相加後的誤差累積

print(0.1 + 0.2 == 0.3)  # False（即使結果看起來像 0.3）
# 這在金融系統中是災難性的

print("\n[Decimal 的解決方案]")
# Decimal：使用十進位精確表示，完全消除捨入誤差
print(Decimal("0.1") + Decimal("0.2"))  # 0.3（完全正確！）
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))  # True

# 重要：必須用字串建立 Decimal，不能用浮點數
# ❌ Decimal(0.1) 仍會引入浮點誤差
# ✓ Decimal("0.1") 精確無誤

print("\n[效能比較]")
# float：快速（使用 CPU 原生指令）
t1 = timeit.timeit(lambda: 0.1 * 999, number=100_000)
# Decimal：精確但慢（純 Python 實現）
t2 = timeit.timeit(lambda: Decimal("0.1") * 999, number=100_000)
print(f"float: {t1:.3f}s  Decimal: {t2:.3f}s（Decimal 約慢 {t2 / t1:.0f} 倍）")
#
# 使用選擇：
#   - float：科學運算、工程計算、機器學習（允許小誤差）
#   - Decimal：金融、會計、精密測量（不允許誤差）
