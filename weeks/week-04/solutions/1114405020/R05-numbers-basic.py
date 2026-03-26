# R05. 數字基礎：四捨五入、進制、格式化（3.1–3.4）
# round / Decimal / format / bin / oct / hex

from decimal import Decimal, localcontext
import math

# ── 3.1 四捨五入 ──────────────────────────────────────
# round(number, ndigits) 的 ndigits 代表「保留到小數第幾位」。
# 下面示範保留 1 位小數：1.27 -> 1.3
print(round(1.27, 1))  # 1.3
# 保留 3 位小數：1.25361 -> 1.254
print(round(1.25361, 3))  # 1.254
# Python 的 round 採用「銀行家捨入（Banker's Rounding）」：
# .5 的情況會捨入到最近的偶數，因此 round(0.5) 是 0。
print(round(0.5))  # 0（銀行家捨入，取最近偶數）
# 同理 2.5 會變成 2（最近偶數）。
print(round(2.5))  # 2

a = 1627731
# 若 ndigits 是負數，會在整數位做四捨五入：
# -1 代表到十位、-2 代表到百位、-3 代表到千位。
print(round(a, -2))  # 1627700（對百位四捨五入）

# ── 3.2 精確浮點數 ────────────────────────────────────
# 一般 float 使用二進位浮點表示，某些十進位小數無法精確表示，
# 所以加法可能出現看似「多出尾巴」的結果。
print(4.2 + 2.1)  # 6.300000000000001（有誤差）
# Decimal 以十進位概念儲存數值，適合金額、精準計算等情境。
# 建議用字串建立 Decimal，避免先被 float 誤差污染。
da, db = Decimal("4.2"), Decimal("2.1")
print(da + db)  # 6.3（精確）

# localcontext 可在 with 區塊中暫時調整 Decimal 的運算設定，
# 這裡把有效精度設定為 3，離開區塊後會恢復原本設定。
with localcontext() as ctx:
    ctx.prec = 3
    print(Decimal("1.3") / Decimal("1.7"))  # 0.765

# math.fsum 修正大數+小數精度
# 一般 sum 在「很大數 + 很小數」混合時，容易讓小數被吃掉；
# math.fsum 使用較穩定的演算法，通常能得到更準確的結果。
print(math.fsum([1.23e18, 1, -1.23e18]))  # 1.0（正確）

# ── 3.3 數字格式化 ────────────────────────────────────
x = 1234.56789
# format(value, spec) 的 spec 可控制小數位數、對齊、分隔符號、科學記號等。
# 0.2f: 固定小數點格式，保留 2 位小數。
print(format(x, "0.2f"))  # '1234.57'
# >10.1f: 右對齊、總寬度 10、保留 1 位小數。
print(format(x, ">10.1f"))  # '    1234.6'
# , : 加入千分位逗號。
print(format(x, ","))  # '1,234.56789'
# 0,.2f: 同時使用千分位與保留 2 位小數。
print(format(x, "0,.2f"))  # '1,234.57'
# e: 科學記號表示法。
print(format(x, "e"))  # '1.234568e+03'

# ── 3.4 二八十六進制 ──────────────────────────────────
n = 1234
# bin / oct / hex 會回傳帶前綴的字串：0b / 0o / 0x。
print(bin(n), oct(n), hex(n))  # 0b10011010010 0o2322 0x4d2
# format 可輸出不帶前綴的進制字串，常用於顯示或序列化。
print(format(n, "b"), format(n, "x"))  # 10011010010 4d2
# int(text, base) 可把不同進制字串轉回十進位整數。
print(int("4d2", 16), int("2322", 8))  # 1234 1234
