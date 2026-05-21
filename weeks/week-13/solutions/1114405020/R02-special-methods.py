# R02. 物件特殊方法
# 讓自訂的 class 表現得像 Python 內建型別
# 對應 Bloom's Taxonomy：記憶（Remember）— 背得出哪個場景用哪個方法

# ── __repr__ 和 __str__：物件的自我介紹 ──────────────────
# __repr__：給「開發者」看的（在 REPL、debug 時出現）
# __str__ ：給「使用者」看的（print() 優先用這個）
#
# 兩者的區別：
#   __repr__ 的目標是「 unambiguous（無歧義）」— 要能重現物件。
#   好的 __repr__ 回傳值通常可以直接貼回 Python REPL 重建該物件。
#
#   __str__ 的目標是「 readable（易讀）」— 讓一般人看得懂。
#   print() 和 str() 會優先呼叫 __str__；若沒定義 __str__，則退而求其次用 __repr__。
#
#   在 REPL 中直接打變數名稱，則只會顯示 __repr__。

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __repr__(self):
        """
        開發者用：回傳一個可以重建物件的字串。
        
        使用 !r 轉換可以確保字串值被正確 quote 起來。
        f"{self.name!r}" → 如果 name="王小明"，輸出 '王小明'（含單引號）
        """
        return f"Student(name={self.name!r}, grade={self.grade})"

    def __str__(self):
        """
        使用者用：回傳一個容易閱讀的字串。
        print() 和 str() 會優先使用這個方法。
        """
        return f"{self.name}：{self.grade} 分"

print("=== __repr__ vs __str__ ===")
s = Student("王小明", 85)
print(repr(s))   # Student(name='王小明', grade=85)  → __repr__
print(str(s))    # 王小明：85 分                        → __str__
print(s)         # 王小明：85 分                        → print 優先用 __str__

# ── __eq__：自訂「相等」的意義 ────────────────────────────
# 沒有 __eq__ 的話，兩個物件只有「同一個記憶體位置」才算相等
#
# Python 的 == 預設使用 is（同一性比較），
# 也就是只有當兩個變數指向同一個記憶體位置時才會回傳 True。
# 對數值或內容相同的物件，我們通常希望它們被視為相等。
#
# __eq__ 的實作慣例：
#   1. 先檢查 other 是否是同一個型別（isinstance）
#   2. 若不是，回傳 NotImplemented（讓 Python 嘗試反過來比對）
#   3. 若是，比較各欄位的值

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        """
        自訂相等條件：當 x 和 y 都相同時，視為相等。
        
        注意回傳 NotImplemented 而非 False 的慣例：
        - 如果 other 不是 Point 型別，我們無法判斷是否相等
        - 回傳 NotImplemented 讓 Python 有機會去呼叫 other.__eq__(self)
        - 若對方也回傳 NotImplemented，Python 才會使用 is 做最後判定
        
        這個機制讓跨型別比較（如 Point(1,2) == (1,2)）有機會正確運作。
        """
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

print("\n=== __eq__：自訂相等條件 ===")
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)
print(p1 == p2)  # True（座標相同，__eq__ 判定相等）
print(p1 == p3)  # False（座標不同）
print(p1 is p2)  # False（是不同的物件，記憶體位置不同）

# ── @total_ordering：自動補齊所有比較運算子 ─────────────
# 只要定義 __eq__ 和一個比較（__lt__），
# @total_ordering 會自動補出 <=, >, >= 四個
#
# 如果一個類別需要完整的比較功能（<, <=, >, >=, ==, !=），
# 通常需要實作 __lt__, __le__, __gt__, __ge__, __eq__, __ne__ 六個方法。
# 但透過 @total_ordering decorator，你只需要實作 __eq__ 和任一個比較方法，
# 其餘四個會由 Python 自動推導出來。
#
# 推導邏輯：
#   a <= b  → a < b or a == b
#   a > b   → not (a < b or a == b)
#   a >= b  → not (a < b)
#   a != b  → not (a == b)

from functools import total_ordering

@total_ordering
class Score:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Score({self.value})"

    def __eq__(self, other):
        """等於：分數相同"""
        return self.value == other.value

    def __lt__(self, other):
        """小於：分數較低（這是 @total_ordering 的基礎比較）"""
        return self.value < other.value

print("\n=== @total_ordering：只寫兩個，自動補齊全部 ===")
a = Score(80)
b = Score(90)
print(a < b)   # True   → __lt__
print(a > b)   # False  → 由 @total_ordering 自動推導（not (a < b or a == b)）
print(a <= b)  # True   → 由 @total_ordering 自動推導（a < b or a == b）

# 因為有了完整的比較功能，Score 可以放進 list 並直接排序
scores = [Score(70), Score(95), Score(60)]
print(sorted(scores))  # [Score(60), Score(70), Score(95)]

# ── __slots__：大量物件時節省記憶體 ──────────────────────
# 一般 class 每個物件都有一個 __dict__，很耗記憶體
# CPE 題目有時會建立幾十萬個小物件，__slots__ 可以大幅節省
#
# 一般物件：每個實例都有一個 __dict__（字典），用來儲存屬性。
# 字典的記憶體開銷很大（因為需要 hash table）。
# __slots__ 告訴 Python：「這個類別只會有這些屬性」，
# Python 就不會為每個物件建立 __dict__，改以類似 tuple 的緊湊結構儲存。
#
# 節省的記憶體隨屬性的數量而異，每個物件大約可節省數十到數百 bytes。
# 對於數十萬個物件的場景，差異非常顯著。

class PointLite:
    __slots__ = ('x', 'y')   # 固定只有這兩個屬性

    def __init__(self, x, y):
        self.x = x
        self.y = y

print("\n=== __slots__：固定屬性，節省記憶體 ===")
p = PointLite(3, 4)
print(p.x, p.y)   # 3 4
# p.z = 5  # 這行會 AttributeError，因為 z 不在 __slots__ 裡
# 因為 __slots__ 固定了屬性名稱，無法動態增加新屬性。
# 這既是優點（節省記憶體）也是限制（缺乏彈性）。

# 記憶重點 ──────────────────────────────────────────────────
# __repr__  → 開發者用，要能「重現」物件
# __str__   → 使用者用，print() 呼叫
# __eq__    → 自訂 == 的意義
# @total_ordering + __lt__ → 自動補齊 <, <=, >, >=
# __slots__ → 固定屬性，大量物件時省記憶體
#
# 其他常用特殊方法（補充）：
#   __len__   → len(obj) 的行為
#   __getitem__ → obj[key] 的行為（支援索引）
#   __setitem__ → obj[key] = value 的行為
#   __iter__  → for x in obj 的行為
#   __call__  → obj() 的行為（讓物件像函數一樣被呼叫）
#   __hash__  → 讓物件可作為 dict 的 key 或放進 set
#   __bool__  → bool(obj) 的行為
#
# 注意事項：
#   1. 若實作 __eq__，通常也應實作 __hash__（否則物件無法放進 set）
#   2. __slots__ 會影響多重繼承的行為（子類別也需定義 __slots__）
#   3. @total_ordering 會稍微降低執行速度（因為是動態推導），
#      在高效能場景建議手動實作所有比較方法
