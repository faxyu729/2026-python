# R06. 特殊數值：無窮大、NaN、分數、隨機（3.7–3.11）
# float inf/nan / fractions.Fraction / random

import math
import random
from fractions import Fraction

# ── 3.7 無窮大與 NaN ──────────────────────────────────
# 使用 float("inf")、float("-inf")、float("nan")
# 可以建立 IEEE 754 的特殊浮點數值。
a = float("inf")
b = float("-inf")
c = float("nan")
print(a, b, c)  # inf -inf nan
# math.isinf(x) 用來判斷 x 是否為正/負無窮大。
print(math.isinf(a))  # True
# math.isnan(x) 用來判斷 x 是否為 NaN（Not a Number）。
print(math.isnan(c))  # True
# 與無窮大運算：
# inf + 45 仍是 inf；有限數 / inf 會趨近 0.0。
print(a + 45, 10 / a)  # inf 0.0
# inf / inf 與 inf + (-inf) 都是未定義，結果為 NaN。
print(a / a, a + b)  # nan nan（未定義）
# NaN 有一個重要特性：它不等於任何值，包含它自己。
# 因此在判斷 NaN 時應使用 math.isnan()，不要用 ==。
print(c == c)  # False（NaN 不等於自己！）

# ── 3.8 分數運算 ──────────────────────────────────────
# Fraction(分子, 分母) 可做「有理數精確運算」，避免浮點誤差。
p = Fraction(5, 4)
q = Fraction(7, 16)
r = p * q
# 分數加法結果會自動約分。
print(p + q)  # 27/16
# 可直接取得分子 numerator 與分母 denominator。
print(r.numerator, r.denominator)  # 35 64
# 需要與其他浮點 API 互動時，可轉為 float。
print(float(r))  # 0.546875
# limit_denominator(max_den) 可找出在指定分母上限下的最佳近似分數。
print(r.limit_denominator(8))  # 4/7
# float.as_integer_ratio() 會回傳可精確表示該 float 的分子分母。
# 用 * 拆包後傳給 Fraction，可把該 float 對應成分數。
print(Fraction(*(3.75).as_integer_ratio()))  # 15/4

# ── 3.11 隨機選擇 ─────────────────────────────────────
values = [1, 2, 3, 4, 5, 6]
# choice: 從序列中隨機取一個元素（可重複呼叫，結果可能重複）。
print(random.choice(values))  # 隨機一個
# sample: 抽 k 個「不重複」樣本，不會改變原序列。
print(random.sample(values, 3))  # 3 個不重複樣本
# shuffle: 就地打亂（in-place），會直接改變 values 本身。
random.shuffle(values)
print(values)  # 打亂後的序列
# randint(a, b): 取得區間 [a, b]（含兩端）的隨機整數。
print(random.randint(0, 10))  # 0~10 整數
# seed 固定後，隨機序列可重現，便於教學、測試與除錯。
random.seed(42)
print(random.random())  # 固定種子：可重現
