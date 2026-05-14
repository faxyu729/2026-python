# R04. 特殊方法（8.2–8.3）
# 主題：__eq__ / __lt__ / __len__ / __contains__ / __iter__
# 版本重點：用步驟化註解說明每一步，理解「語法糖背後呼叫了哪個特殊方法」。

from functools import total_ordering

# ── 步驟 0：用 @total_ordering 建立可比較的 Score 類別 ───
# 目的：讓自訂物件可使用 >、<、>=、<=、==、!= 與 sorted()。
# 作法：只定義 __eq__ 和 __lt__，其餘比較方法交給 total_ordering 自動補齊。
# 結果：程式碼更精簡，且比較語意一致。
@total_ordering
class Score:
    # 子步驟 0-1：初始化資料欄位。
    def __init__(self, name, value):
        self.name = name
        self.value = value

    # 子步驟 0-2：除錯顯示字串。
    def __repr__(self):
        return f"Score({self.name!r}, {self.value})"

    # 子步驟 0-3：定義相等判斷（==）。
    # 若型別不相容，回傳 NotImplemented，讓 Python 嘗試其他比較路徑。
    def __eq__(self, other):
        if not isinstance(other, Score):
            return NotImplemented
        return self.value == other.value

    # 子步驟 0-4：定義小於判斷（<）。
    # 本例以 value 作為排序依據。
    def __lt__(self, other):
        if not isinstance(other, Score):
            return NotImplemented
        return self.value < other.value


# ── 步驟 1：建立 Score 實例並測試比較運算 ───────────────
# 目的：驗證 total_ordering 是否成功補齊其他比較行為。
# 子步驟 1-1：建立三筆成績資料。
s1 = Score("Alice", 90)
s2 = Score("Bob", 75)
s3 = Score("Carol", 90)

# 子步驟 1-2：比較運算示範。
# 說明：s1 > s2 會透過 __lt__ 與 total_ordering 產生的邏輯推導。
print(s1 > s2)      # True  （由 __lt__ 推導）
print(s1 == s3)     # True
print(s1 != s2)     # True  （由 __eq__ 推導）

# 子步驟 1-3：sorted() 需要可比較物件，會用到 __lt__。
print(sorted([s1, s2, s3]))     # 升冪排列

# ── 步驟 2：建立容器類別 Classroom，實作容器協定 ─────────
# 目的：讓自訂類別能像內建容器一樣支援 len()、in、for。
# 作法：實作 __len__、__contains__、__iter__。
# 結果：可直接使用 Python 常見語法操作 Classroom。
class Classroom:
    # 子步驟 2-1：初始化班級名稱與內部學生清單。
    def __init__(self, name):
        self.name = name
        self._students = []

    # 子步驟 2-2：提供新增學生方法。
    def add(self, student):
        self._students.append(student)

    # 子步驟 2-3：讓 len(obj) 可用。
    def __len__(self):
        return len(self._students)

    # 子步驟 2-4：讓 x in obj 可用。
    def __contains__(self, student):
        return student in self._students

    # 子步驟 2-5：讓 for x in obj 可用。
    # 回傳一個可迭代器（iterator）。
    def __iter__(self):
        return iter(self._students)

    # 子步驟 2-6：定義物件表示字串，並示範可在 __repr__ 內呼叫 len(self)。
    def __repr__(self):
        return f"Classroom({self.name!r}, {len(self)} 人)"


# ── 步驟 3：驗證 Classroom 容器行為 ──────────────────────
# 目的：確認 __len__ / __contains__ / __iter__ 真的被語法觸發。
# 子步驟 3-1：建立班級並加入學生。
cls = Classroom("資工一甲")
cls.add("Alice")
cls.add("Bob")
cls.add("Carol")

# 子步驟 3-2：len(cls) -> 呼叫 __len__。
print(len(cls))             # 3

# 子步驟 3-3："Alice" in cls -> 呼叫 __contains__。
print("Alice" in cls)       # True
print("Dave" in cls)        # False

# 子步驟 3-4：for student in cls -> 呼叫 __iter__。
for student in cls:         # __iter__ 讓 for 迴圈可用
    print(student)

# 學習路徑建議：
# 1. 先掌握 __eq__ / __lt__ 與 total_ordering 的搭配
# 2. 再理解 NotImplemented 在型別不相容比較時的角色
# 3. 最後練習容器協定（__len__ / __contains__ / __iter__）
