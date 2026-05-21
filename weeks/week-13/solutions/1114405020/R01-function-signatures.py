# R01. 函數彈性簽章
# 讓函數可以接受「不固定數量」的參數
# 對應 Bloom's Taxonomy：記憶（Remember）— 背得出語法

# ── *args：不定個數的位置參數 ─────────────────────────────
# 問題：想加總任意幾個數字，不知道會有幾個
#
# *args 的運作原理：
#   當你在函數定義的參數前面加上一個星號（*），
#   Python 會把「所有多餘的位置引數」打包成一個 tuple 傳給這個參數。
#
#   例如：add_all(1, 2, 3, 4, 5)
#   → args = (1, 2, 3, 4, 5)，是一個 tuple
#
#   慣例上命名為 args（arguments），但實際上可以用任何名稱。
#   重點是星號 *，不是名稱 args。

def add_all(*args):
    """args 在函數內是一個 tuple"""
    return sum(args)

print("=== *args：不定個數的位置參數 ===")
print(add_all(1, 2))            # 3        → args = (1, 2)
print(add_all(1, 2, 3, 4, 5))  # 15       → args = (1, 2, 3, 4, 5)
print(add_all())                # 0（空的也沒問題）→ args = ()

# ── **kwargs：不定個數的關鍵字參數 ───────────────────────
# kwargs 在函數內是一個 dict
#
# **kwargs 的運作原理：
#   當你在函數定義的參數前面加上兩個星號（**），
#   Python 會把「所有多餘的關鍵字引數」打包成一個 dict 傳給這個參數。
#
#   例如：make_student(name="王小明", grade=85, seat=12)
#   → kwargs = {"name": "王小明", "grade": 85, "seat": 12}
#
#   *args 和 **kwargs 可以同時使用，順序必須是：
#   普通參數 → *args → keyword-only → **kwargs

def make_student(**kwargs):
    """建立學生資料，欄位可以自由指定"""
    return kwargs

print("\n=== **kwargs：不定個數的關鍵字參數 ===")
s = make_student(name="王小明", grade=85, seat=12)
print(s)   # {'name': '王小明', 'grade': 85, 'seat': 12}

# ── keyword-only：強制用名稱呼叫 ─────────────────────────
# * 後面的參數「一定要具名」，避免填錯順序
#
# 有時候函數的參數數量固定，但希望呼叫者「一定要用名稱來指定」。
# 只要在參數清單中放一個單獨的星號（*），
# 星號「之後」的所有參數都變成 keyword-only（強制具名）。
#
# 這對於容易搞混順序的參數特別有用，
# 例如 subject 和 score 都是數字或字串，不小心交換了也不會報錯。
# 強制具名後，呼叫者一定要寫 subject="數學", score=90，
# 就不會搞錯順序了。

def send_score(student_id, *, subject, score):
    """* 之後的參數必須具名，避免搞混"""
    print(f"學號 {student_id}｜{subject}：{score} 分")

print("\n=== keyword-only：強制具名，避免填錯順序 ===")
send_score("411234001", subject="數學", score=90)   # 正確
# send_score("411234001", "數學", 90)  # ← 這樣會 TypeError！
# 因為 subject 和 score 在 * 後面，必須用 keyword 傳遞

# ── 三種參數混合使用 ──────────────────────────────────────
def report(title, *scores, prefix="成績"):
    """title 普通參數，scores 不定個數，prefix 有預設值"""
    avg = sum(scores) / len(scores) if scores else 0
    print(f"{prefix}報告－{title}：平均 {avg:.1f}")

print("\n=== 混合：普通 + *args + 預設值 ===")
report("期中考", 80, 90, 70)
report("期末考", 95, 85, 75, 100, prefix="最終")

# ── 記憶重點 ──────────────────────────────────────────────
# *args   → tuple，接受任意個「值」
# **kwargs → dict，接受任意個「名稱=值」
# *（單獨）→ 後面的參數一定要具名
# 順序：普通參數 → *args → keyword-only → **kwargs
#
# 進階補充：
#   1. 參數解包（argument unpacking）：
#      呼叫時也可以使用 * 和 **，功能與定義時相反：
#      - *iterable  → 將可疊代物件展開為位置引數
#      - **mapping  → 將 dict 展開為關鍵字引數
#      例如：nums = [1, 2, 3]; add_all(*nums) 相當於 add_all(1, 2, 3)
#
#   2. / （positional-only）：
#      Python 3.8+ 新增了「純位置參數」語法。
#      在 / 之前的參數只能用位置傳遞，不能用關鍵字。
#      例如：def f(a, b, /, c): ...
#      只能寫 f(1, 2, c=3) 或 f(1, 2, 3)
#      不能寫 f(a=1, b=2, c=3)
#
#   3. 組合範例：
#      def full_func(a, b, /, c, *args, d, **kwargs): ...
#      a, b    : positional-only（只能按位置傳）
#      c       : 普通參數（位置或關鍵字皆可）
#      *args   : 額外位置參數
#      d       : keyword-only（一定要具名）
#      **kwargs: 額外關鍵字參數
