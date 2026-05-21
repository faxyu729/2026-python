# U02. @classmethod：多重構造器（工廠方法）
# 讓 class 可以用「不同格式的資料」建立物件，不只是靠 __init__
# 對應 Bloom's Taxonomy：理解（Understand）— 能解釋 cls 的作用與繼承行為

# ── 問題：__init__ 只能有一種寫法 ────────────────────────
# 座標點可能來自不同地方：
#   - 直接給 (x, y)
#   - 從字串 "3,4" 解析
#   - 從 list [3, 4] 讀取
# 三種都用 __init__ 處理，會讓 __init__ 變得很複雜
#
# 不好的做法：在 __init__ 裡用 type checking 決定如何解析
#   def __init__(self, x, y=None):
#       if y is None and isinstance(x, str):
#           x, y = map(int, x.split(','))
#       ...
#   → __init__ 的參數變得模糊，無法從 signature 知道該傳什麼

# ── @classmethod 解法：每種格式一個工廠方法 ─────────────
class Point:
    """
    Point class 示範 @classmethod 的多重構造器。
    
    @classmethod 的特性：
      1. 第一個參數是 cls（class 本身），不是 self（實例）
      2. 可以在不建立物件的情況下呼叫（與 @staticmethod 類似）
      3. cls(...) 等同於呼叫 __init__，建立並回傳新物件
      4. 在繼承時，cls 會指向「實際被呼叫的子類」，而不是定義時的父類
    """

    def __init__(self, x, y):
        """
        基礎構造器：直接接收 x, y 座標。
        
        這是物件的「主要構造器」（primary constructor），
        所有的 @classmethod 最終都會透過 cls(x, y) 回到這裡。
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """開發者用：回傳可重建物件的字串表示"""
        return f"Point({self.x}, {self.y})"

    @classmethod
    def from_string(cls, s):
        """
        從 '3,4' 這種逗號分隔的字串建立 Point。
        
        使用方式：Point.from_string("3,4")
        
        流程：
          1. s.split(',') → ["3", "4"]
          2. map(int, ...) → [3, 4]
          3. cls(3, 4) → 回傳 Point(3, 4)
        
        注意：這裡用的是 cls 而不是 Point，
        在繼承的情境下 cls 會自動變成子類別。
        """
        # cls 就是「目前的 class 本身」，等於 Point
        x, y = map(int, s.split(','))
        return cls(x, y)

    @classmethod
    def from_list(cls, lst):
        """
        從 [3, 4] 這種 list 建立 Point。
        
        使用方式：Point.from_list([3, 4])
        
        注意：
          - 這裡沒有做邊界檢查，如果 lst 長度不足會拋出例外
          - 實務上可加入 len(lst) >= 2 的檢查
        """
        return cls(lst[0], lst[1])

    @classmethod
    def origin(cls):
        """
        原點的工廠方法。
        
        使用方式：Point.origin()
        
        這是一個「無參數」的工廠方法，
        提供語意明確的方式來建立原點物件，
        比 Point(0, 0) 更具可讀性。
        """
        return cls(0, 0)

print("=== @classmethod 多重構造器 ===")
p1 = Point(3, 4)                   # 一般方式
p2 = Point.from_string("3,4")     # 從字串
p3 = Point.from_list([3, 4])      # 從 list
p4 = Point.origin()               # 工廠方法
print(p1, p2, p3, p4)

# ── cls 在繼承時很重要 ────────────────────────────────────
# from_string 繼承自 Point，但 cls 會指向「實際呼叫的 class」
#
# 關鍵概念：
#   如果 from_string 裡面寫的是 return Point(x, y) 而非 cls(x, y)，
#   那麼即使透過 ColoredPoint.from_string("5,6") 呼叫，
#   回傳的也會是 Point 物件，而不是 ColoredPoint 物件。
#
#   使用 cls 確保了：
#     - Point.from_string(...)  回傳 Point
#     - ColoredPoint.from_string(...) 回傳 ColoredPoint
#   這就是「多型工廠方法」的實作關鍵。

class ColoredPoint(Point):
    """
    ColoredPoint 繼承 Point，擴充了 color 屬性。
    
    因為 Point 的 @classmethod 使用 cls 而非寫死的 Point，
    所以 ColoredPoint 不需要重新定義 from_string / from_list / origin，
    直接繼承就能正確運作。
    """

    def __init__(self, x, y, color="black"):
        """
        擴充 __init__：在 x, y 之外增加 color 屬性。
        
        注意：因為 factory method 會呼叫 cls(x, y)，
        而 ColoredPoint.__init__ 需要三個參數 (self, x, y, color="black")，
        這裡 color 有預設值 "black"，所以 cls(x, y) 可以正常運作。
        """
        super().__init__(x, y)   # 呼叫 Point.__init__ 設定 x, y
        self.color = color

    def __repr__(self):
        return f"ColoredPoint({self.x}, {self.y}, color={self.color!r})"

print("\n=== 繼承時 cls 指向子類 ===")
cp = ColoredPoint.from_string("5,6")
print(cp)            # ColoredPoint(5, 6, color='black')
print(type(cp))      # <class '__main__.ColoredPoint'>，不是 Point！
# 驗證：cp 確實是 ColoredPoint 實例，不是 Point 實例
# 這證明 from_string 內部的 cls(...) 正確使用了子類別

# ── CPE 應用：UVA 11005 進位制物件 ──────────────────────
# 題目的輸入是一串成本值，可以用 classmethod 從字串建立
#
# UVA 11005 題目簡述：
#   每個數字字元（0-9, A-Z）有不同的印刷成本。
#   給定一個十進位數字 n，要找出在 2~36 進位中，
#   哪個進位的總印刷成本最低。
#
#   輸入格式：第一行是 36 個整數（每個字元的成本），
#   後面有若干行，每行一個要計算的 n。
#   用 @classmethod 可以輕鬆從不同格式建立 CostTable 物件。

class CostTable:
    """儲存 36 個字元（0-9, A-Z）各自的印刷成本"""

    CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, costs):
        """
        基礎構造器：接收完整的成本串列。
        
        參數：
            costs : list[int] — 長度 36 的成本表，
                    costs[0] 是 '0' 的成本，...，costs[35] 是 'Z' 的成本
        """
        self.costs = costs   # list，長度 36

    def cost_of(self, digit_index):
        """取得第 digit_index 個字元的成本"""
        return self.costs[digit_index]

    def total_cost(self, n, base):
        """
        計算數字 n 在 base 進位下的總印刷成本。
        
        演算法：
          1. 若 n == 0，直接回傳 costs[0]（數字 0 的成本）
          2. 否則反覆：
             total += costs[n % base]    ← 累加當前最低位數字的成本
             n //= base                   ← 右移一位
          3. 直到 n == 0
        
        參數：
            n    : int — 要計算的十進位數字
            base : int — 目標進位（2~36）
        
        回傳值：
            int — 在該進位下的總成本
        """
        if n == 0:
            return self.costs[0]
        total = 0
        while n > 0:
            total += self.costs[n % base]
            n //= base
        return total

    @classmethod
    def uniform(cls, cost=1):
        """
        建立所有字元成本相同的表（方便測試）。
        
        使用方式：CostTable.uniform(1)
        
        適合在開發測試時快速建立一個等成本表，
        不需要每次從輸入檔讀取 36 個數字。
        """
        return cls([cost] * 36)

    @classmethod
    def from_flat_string(cls, s):
        """
        從一行 36 個整數（空白分隔）建立成本表。
        
        使用方式：CostTable.from_flat_string("1 2 3 ... 36")
        
        這正是 UVA 11005 的輸入格式，一個 @classmethod 直接對應。
        """
        values = list(map(int, s.split()))
        return cls(values)

print("\n=== CPE：進位制成本計算 ===")
table = CostTable.uniform(1)   # 每個字元成本都是 1
n = 255
for base in range(2, 11):
    c = table.total_cost(n, base)
    print(f"  255 在 {base:2d} 進位：位數 {c}")

# 記憶重點 ──────────────────────────────────────────────────
# @classmethod 的第一個參數是 cls（class 本身），不是 self（物件）
# cls(...)  等於  ClassName(...)，但繼承時會自動用子類
# 常用於：替代構造器、工廠方法、從不同格式解析資料
#
# @classmethod vs @staticmethod 的比較：
#
#   @classmethod                    @staticmethod
#   ─────────────────────────────────────────────────
#   接收 cls 參數                   不收 cls 或 self
#   可存取 class 變數（如 COST_CHARS）  無法存取 class 變數
#   支援繼承多型（cls 會指向子類）   不支援繼承多型（寫死哪個 class）
#   可建立並回傳實例                 通常只做工具函數（如轉換）
#
# 使用選擇：
#   需要建立物件 → @classmethod
#   純工具函數（不須存取 class）→ @staticmethod
#   需要存取實例屬性 → 一般實例方法
