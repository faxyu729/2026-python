# R02. 屬性封裝（8.6）
# @property / getter / setter / 唯讀屬性
#
# Python 的 @property 裝飾器（decorator）提供一種「優雅的封裝」方式，
# 讓方法的存取語法看起來就像一般屬性存取，同時可以在背後加入驗證、
# 計算或唯讀邏輯。這是 Python 實踐封裝（encapsulation）的主流手法。

# ── 基本 @property ────────────────────────────────────────

class Circle:
    """圓形類別，示範 @property 的基本用法：getter、setter 與唯讀屬性。"""

    def __init__(self, radius):
        # _radius：底線開頭的屬性屬於「受保護」（protected）慣例，
        # 提醒開發者「請透過 property 存取，不要直接修改」。
        # 這是約定而非強制，Python 沒有真正的 private。
        self._radius = radius

    @property
    def radius(self):
        """radius 的 getter（讀取器）：取得半徑值。
        @property 裝飾器讓 radius() 方法可以像屬性一樣被讀取（c.radius）。"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """radius 的 setter（寫入器）：設定半徑值，並進行驗證。
        @radius.setter 裝飾器讓 c.radius = value 的賦值行為被攔截。"""
        if value < 0:
            raise ValueError("半徑不能為負數")
        self._radius = value

    @property
    def area(self):
        """圓面積（唯讀屬性）：只有 getter 沒有 setter。
        嘗試 c.area = 100 會觸發 AttributeError。
        此處每次存取都會重新計算，適合簡單運算。"""
        import math
        return math.pi * self._radius ** 2

    @property
    def diameter(self):
        """直徑（唯讀屬性）：半徑的兩倍。"""
        return self._radius * 2


c = Circle(5)        # 建立半徑為 5 的圓
print(c.radius)      # 5    — 透過 getter 讀取，語法像一般屬性
print(c.area)        # 78.539... — 唯讀的計算屬性
print(c.diameter)    # 10   — 另一個唯讀計算屬性

c.radius = 10        # 透過 setter 賦值，背後會執行驗證邏輯
print(c.area)        # 314.159... — 半徑改變後面積自動更新

try:
    c.radius = -1    # 觸發 ValueError，因為 setter 中拒絕負數
except ValueError as e:
    print(e)         # 半徑不能為負數

try:
    c.area = 100     # 嘗試對唯讀屬性賦值，觸發 AttributeError
except AttributeError as e:
    print(e)         # can't set attribute

# ── 用 property 做延遲計算 ────────────────────────────────

class Rectangle:
    """矩形類別，示範 @property 用於即時計算的屬性。
    此設計的好處：修改 width 或 height 後，area 與 perimeter 自動更新。"""

    def __init__(self, width, height):
        self.width = width        # 此處直接使用公開屬性（未封裝）
        self.height = height      # 因為不需要驗證邏輯，直接賦值即可

    @property
    def area(self):
        """面積 = 寬 × 高，每次讀取即時計算。"""
        return self.width * self.height

    @property
    def perimeter(self):
        """周長 = 2 × (寬 + 高)。"""
        return 2 * (self.width + self.height)


r = Rectangle(4, 6)
print(r.area)       # 24  — 4 × 6
print(r.perimeter)  # 20  — 2 × (4 + 6)
r.width = 8         # 修改寬度
print(r.area)       # 48  — 8 × 6，property 自動反映最新值，無需手動更新
