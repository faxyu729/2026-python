# R02. 屬性封裝（8.6）
# 主題：@property / getter / setter / 唯讀屬性 / 延遲計算
# 版本重點：用步驟化註解拆解每一步，方便教學與複習。

# ── 步驟 0：建立 Circle 類別，示範基本封裝 ───────────────
# 目的：讓外部以「屬性語法」讀寫資料，但內部可加入驗證邏輯。
# 作法：用 _radius 作為內部儲存欄位，對外透過 radius property 存取。
# 結果：外部寫 c.radius = x 時會自動走 setter，不需直接碰 _radius。
class Circle:
    # 子步驟 0-1：初始化內部欄位。
    # _radius 依慣例表示「內部使用」，通常不建議外部直接修改。
    def __init__(self, radius):
        self._radius = radius   # _radius：慣例上表示「受保護」，不直接存取

    # 子步驟 0-2：getter（讀取屬性）
    # 使用方式：c.radius（看起來像屬性，其實會呼叫這個方法）。
    @property
    def radius(self):
        return self._radius

    # 子步驟 0-3：setter（設定屬性）
    # 使用方式：c.radius = value（會先經過這裡驗證）。
    @radius.setter
    def radius(self, value):
        # 加入資料驗證：半徑不可為負。
        if value < 0:
            raise ValueError("半徑不能為負數")
        self._radius = value

    # 子步驟 0-4：唯讀屬性 area
    # 沒有對應 setter，所以只能讀不能設。
    @property
    def area(self):             # 唯讀屬性（沒有 setter）
        import math
        return math.pi * self._radius ** 2

    # 子步驟 0-5：另一個唯讀屬性 diameter
    # 由 _radius 即時計算，不需額外儲存。
    @property
    def diameter(self):
        return self._radius * 2


# ── 步驟 1：建立 Circle 實例並觀察 property 行為 ──────────
# 目的：驗證 getter / setter / 唯讀屬性的實際效果。
# 子步驟 1-1：建立物件。
c = Circle(5)

# 子步驟 1-2：讀取 radius，實際會呼叫 getter。
print(c.radius)     # 5

# 子步驟 1-3：讀取 area、diameter，會即時計算回傳。
print(c.area)       # 78.539...
print(c.diameter)   # 10

# 子步驟 1-4：設定 radius，實際會呼叫 setter 進行驗證與更新。
c.radius = 10       # 呼叫 setter
# 更新後 area 會自動反映新半徑（不需手動同步）。
print(c.area)       # 314.159...

# 子步驟 1-5：嘗試非法值，確認會拋出 ValueError。
try:
    c.radius = -1   # 觸發 ValueError
except ValueError as e:
    print(e)        # 半徑不能為負數

# 子步驟 1-6：嘗試寫入唯讀屬性，確認會拋出 AttributeError。
try:
    c.area = 100    # 唯讀屬性不能設定
except AttributeError as e:
    print(e)

# ── 步驟 2：用 property 做延遲計算（Rectangle）───────────
# 目的：示範「不儲存結果，只在被存取時即時計算」的模式。
# 作法：只儲存 width/height，area/perimeter 用 @property 動態算。
# 結果：任何尺寸變更後，面積與周長都會自動反映最新值。
class Rectangle:
    # 子步驟 2-1：初始化基本尺寸。
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # 子步驟 2-2：面積屬性（延遲計算）
    @property
    def area(self):
        return self.width * self.height

    # 子步驟 2-3：周長屬性（延遲計算）
    @property
    def perimeter(self):
        return 2 * (self.width + self.height)


# ── 步驟 3：驗證 Rectangle 屬性會隨欄位變更自動更新 ─────
# 子步驟 3-1：建立矩形並讀取初始值。
r = Rectangle(4, 6)
print(r.area)       # 24
print(r.perimeter)  # 20

# 子步驟 3-2：改變 width 後再次讀取 area。
# 因為 area 是即時計算，所以不需要重新指定任何快取值。
r.width = 8         # 修改後 area 自動更新
print(r.area)       # 48

# 學習路徑建議：
# 1. 先理解 _radius 與 radius property 的角色分工
# 2. 再熟悉 getter/setter 如何加入驗證
# 3. 最後掌握唯讀屬性與延遲計算在實務上的維護優勢
