# R01. 類別基礎（8.1）
# __init__ / 方法 / __repr__ / __str__
#
# Python 的類別（class）是物件導向程式設計的核心機制。
# 透過 class 關鍵字定義藍圖，再透過建構子建立實際的物件（實例）。
# 本檔案示範：建構子 __init__、實例方法、以及兩個重要的特殊方法
# __repr__ 與 __str__ 的區別。

# ── 最簡單的 class ────────────────────────────────────────

class Point:
    """二維平面上的點，示範最基本的類別定義。"""

    def __init__(self, x, y):
        """建構子（constructor）：建立實例時自動呼叫。
        self 代表「這個實例本身」，是 Python 方法的第一個參數。
        透過 self.x = x 將傳入的參數儲存為實例變數（instance variable）。"""
        self.x = x
        self.y = y

    # __repr__：給開發者看，eval() 能重建物件最理想
    def __repr__(self):
        """給開發者觀看的正式字串表示法（representation）。
        優先於 __str__ 被呼叫。若類別未定義 __str__，print() 也會使用 __repr__。
        慣例上應回傳一個能重建相同物件的 Python 表達式字串。"""
        return f"Point({self.x}, {self.y})"

    # __str__：給使用者看，print() 時呼叫
    def __str__(self):
        """給使用者觀看的非正式字串表示法。
        print()、str() 及 f-string 會優先呼叫 __str__。
        若未定義 __str__，則會退而使用 __repr__。"""
        return f"({self.x}, {self.y})"

    def distance_to(self, other):
        """計算目前點到另一個點（other）的歐幾里得距離。
        使用畢氏定理：√((x2-x1)² + (y2-y1)²)
        ** 0.5 相當於開平方根。"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


p1 = Point(0, 0)  # 建立原點 (0, 0)
p2 = Point(3, 4)  # 建立點 (3, 4)

print(repr(p1))            # 呼叫 Point.__repr__，輸出 Point(0, 0)
print(str(p2))             # 呼叫 Point.__str__，輸出 (3, 4)
print(p1.distance_to(p2))  # 計算 (0,0) 到 (3,4) 的距離，結果為 5.0

# ── 類別變數 vs 實例變數 ──────────────────────────────────

class Student:
    """學生類別，示範類別變數（class variable）與實例變數（instance variable）的差異。"""

    school = "國立澎湖科技大學"    # 類別變數：所有實例共用，定義在類別區塊內但不在方法內

    def __init__(self, name, student_id):
        self.name = name            # 實例變數：每個實例獨立，透過 self 綁定
        self.student_id = student_id

    def __repr__(self):
        """回傳正式字串，方便除錯時辨識學生物件。"""
        return f"Student({self.student_id}, {self.name})"

    def greeting(self):
        """回傳問候語，示範在實例方法中存取類別變數 self.school。"""
        return f"我是 {self.school} 的 {self.name}"


s1 = Student("王小明", "11144050001")
s2 = Student("李小華", "11144050002")

print(s1.greeting())       # 存取實例方法，內部使用了類別變數 school
print(s2.school)           # 透過實例存取類別變數（Python 會往上找到類別屬性）
print(Student.school)      # 透過類別名稱直接存取類別變數

# 修改類別變數影響所有實例
Student.school = "NPU"     # 修改的是類別本身的屬性
print(s1.school)           # NPU — 所有實例反映此變更
print(s2.school)           # NPU — 因為類別變數由所有實例共用
