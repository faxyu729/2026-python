# R01. 類別基礎（8.1）
# 主題：__init__ / 方法 / __repr__ / __str__ / 類別變數與實例變數
# 版本重點：用步驟化註解，逐段說明每一步的目的、作法、結果。

# ── 步驟 0：建立第一個類別 Point ─────────────────────────
# 目的：用最小範例理解「類別像藍圖，實例像成品」。
# 作法：定義座標點 Point，包含 x、y 與常用方法。
# 結果：可建立點、列印點、計算兩點距離。
class Point:
    # 子步驟 0-1：初始化方法 __init__
    # 每次建立 Point(x, y) 時會自動呼叫，將資料存進實例屬性。
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 子步驟 0-2：__repr__
    # 目的：給開發者看，偏向除錯與診斷用途。
    # 理想情況是回傳可重建物件的字串形式（本範例接近此概念）。
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    # 子步驟 0-3：__str__
    # 目的：給使用者看，偏向友善顯示。
    # print(obj) 時會優先使用 __str__。
    def __str__(self):
        return f"({self.x}, {self.y})"

    # 子步驟 0-4：一般實例方法
    # 目的：示範方法如何使用 self 與另一個物件 other。
    # 作法：套用平面距離公式。
    # 結果：回傳兩點的歐幾里得距離（浮點數）。
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# ── 步驟 1：建立 Point 實例並測試方法 ────────────────────
# 目的：驗證 __repr__ / __str__ / distance_to 的實際輸出。
# 子步驟 1-1：建立兩個點 p1、p2。
p1 = Point(0, 0)
p2 = Point(3, 4)

# 子步驟 1-2：repr(p1) 呼叫 __repr__。
print(repr(p1))             # Point(0, 0)

# 子步驟 1-3：str(p2) 呼叫 __str__。
print(str(p2))              # (3, 4)

# 子步驟 1-4：計算距離，3-4-5 三角形結果應為 5.0。
print(p1.distance_to(p2))  # 5.0

# ── 步驟 2：類別變數 vs 實例變數 ─────────────────────────
# 目的：理解「全體共用」與「個別擁有」的差異。
# 作法：定義 Student 類別，讓 school 當類別變數，name/student_id 當實例變數。
# 結果：可觀察修改類別變數後，所有實例都會受到影響。
class Student:
    # 子步驟 2-1：類別變數（所有實例共用同一份）
    school = "國立澎湖科技大學"    # 類別變數：所有實例共用

    # 子步驟 2-2：實例初始化（每個學生各自擁有）
    def __init__(self, name, student_id):
        self.name = name            # 實例變數：每個實例獨立
        self.student_id = student_id

    # 子步驟 2-3：提供開發者可讀表示
    def __repr__(self):
        return f"Student({self.student_id}, {self.name})"

    # 子步驟 2-4：方法中同時使用類別變數與實例變數
    def greeting(self):
        return f"我是 {self.school} 的 {self.name}"


# ── 步驟 3：建立 Student 實例並觀察存取方式 ───────────────
# 子步驟 3-1：建立兩位學生。
s1 = Student("王小明", "11144050001")
s2 = Student("李小華", "11144050002")

# 子步驟 3-2：呼叫實例方法 greeting()。
print(s1.greeting())

# 子步驟 3-3：透過實例存取類別變數（語法可行）。
print(s2.school)            # 透過實例存取類別變數

# 子步驟 3-4：透過類別名稱存取類別變數（較清楚）。
print(Student.school)       # 透過類別名稱存取

# ── 步驟 4：修改類別變數，觀察全體影響 ───────────────────
# 目的：驗證類別變數是共享資料。
# 作法：直接改 Student.school。
# 結果：未覆寫同名實例屬性的所有學生，都會看到新值。
Student.school = "NPU"
print(s1.school)            # NPU
print(s2.school)            # NPU

# 學習路徑建議：
# 1. 先熟悉 __init__ / self 與實例建立
# 2. 再理解 __repr__ 與 __str__ 使用場景
# 3. 最後掌握類別變數與實例變數差異，避免共享資料誤用
