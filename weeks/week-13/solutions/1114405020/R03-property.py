# R03. @property：屬性的守門員
# 讓 class 的屬性在「讀取」或「設定」時可以加入驗證邏輯
# 對應 Bloom's Taxonomy：記憶（Remember）— 背得出語法與使用時機

# ── 沒有保護的屬性會怎樣？ ───────────────────────────────
#
# 問題說明：
#   在 Python 中，物件的屬性（attribute）預設是完全公開的。
#   外部程式碼可以直接讀取和修改任何屬性，沒有任何攔截機制。
#
#   這在簡單的資料容器（如 NamedTuple、DataClass）中沒問題，
#   但當屬性需要「有意義的約束」時（如成績只能在 0~100），
#   直接暴露屬性就無法防止錯誤的賦值。

class BadStudent:
    """
    反例：完全沒有保護的 class。
    
    這個 class 的問題：
      grade 屬性可以被設為任何值，包含不合邏輯的 -100。
      沒有人可以阻止這個錯誤，因為 Python 沒有內建的屬性保護機制。
    
    解決方案：@property
      用 getter/setter 模式在不改變外部 API（s.grade）的前提下，
      在讀取和寫入時插入驗證邏輯。
    """

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade   # 任何值都能塞進去

s = BadStudent("王小明", 85)
s.grade = -100   # 竟然可以！成績不能是負數
print(f"糟糕：{s.name} 的成績是 {s.grade}")  # -100

# ── @property：在存取屬性時加上檢查 ─────────────────────
#
# @property 的運作原理：
#   Python 的 @property 是一個 decorator，它將一個方法轉換成「唯讀屬性」。
#   加上 @屬性名.setter 後，這個屬性就可以被賦值。
#
#   從外部看起來，grade 仍然只是一個簡單的屬性（s.grade = xxx），
#   但實際上 Python 會自動呼叫對應的 getter/setter 方法。
#
#   命名慣例：
#     公開屬性名：grade（給外部用的名稱）
#     私有儲存：_grade（底線開頭，表示「內部使用，請勿直接存取」）
#
#   這稱為「統一存取原則」（Uniform Access Principle）：
#     無論屬性是直接儲存還是計算得來，外部都使用相同的語法存取。
#     你可以在不改變外部 API 的前提下，從「直接屬性」改為「方法計算」。

class Student:
    """
    使用 @property 保護成績屬性的 Student class。
    
    設計目標：
      1. 外部仍然使用 s.grade 讀取，s.grade = xxx 設定
      2. 賦值時自動檢查數值是否在 0~100 之間
      3. 不合法的值觸發 ValueError，而非默默接受
    """

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade   # 這裡會自動呼叫下面的 setter

    @property
    def grade(self):
        """
        getter：讀取 self.grade 時自動呼叫。
        
        當外部程式碼執行 s.grade 時，Python 會呼叫這個方法。
        這個方法回傳 _grade 的實際值。
        
        為什麼不回傳 self.grade？
          如果寫 return self.grade，會再次觸發 grade getter，
          造成無限遞迴 → RecursionError。
          所以實際資料必須存在不同的名稱（_grade）中。
        """
        return self._grade   # 實際資料存在 _grade（底線代表「內部用」）

    @grade.setter
    def grade(self, value):
        """
        setter：執行 self.grade = xxx 時自動呼叫。
        
        參數：
            value : int — 要設定的成績值
        
        驗證邏輯：
          1. 0 <= value <= 100
          2. 若不合法，拋出 ValueError
          3. 若合法，存入 self._grade
        
        注意：這個 setter 也在 __init__ 中被呼叫，
        因為 __init__ 裡寫了 self.grade = grade。
        """
        if not (0 <= value <= 100):
            raise ValueError(f"成績必須在 0～100，你給了 {value}")
        self._grade = value

print("\n=== @property 守門員 ===")
s = Student("李大華", 90)
print(s.grade)    # 90 → 自動呼叫 grade getter

s.grade = 75      # 合法，通過檢查 → 自動呼叫 grade setter
print(s.grade)    # 75

try:
    s.grade = -10  # 觸發 ValueError（setter 檢查不通過）
except ValueError as e:
    print(f"錯誤：{e}")

# ── 唯讀屬性：計算出來的值不需要存 ──────────────────────
#
# 有些屬性不需要真的儲存，而是由其他屬性計算得出。
# 例如圓形的「面積」由半徑決定，不需要獨立的記憶體空間。
#
# 使用 @property 定義唯讀屬性：
#   - 只有 getter，沒有 setter
#   - 外部可以讀取，但不能寫入
#   - 每次讀取都重新計算（保證與相依屬性同步）

class Circle:
    """
    圓形 class，示範唯讀計算屬性。
    
    radius 是一般屬性（可讀寫），
    area 和 diameter 是唯讀屬性（由 radius 計算得來）。
    
    優點：
      - 修改 radius 後，area 和 diameter 自動更新
      - 不需要手動更新或快取
      - 不佔用獨立記憶體
    """

    def __init__(self, radius):
        self.radius = radius   # radius 是一般屬性（公開的）

    @property
    def area(self):
        """
        面積是計算出來的，不該被直接設定。
        
        公式：π × r²
        
        注意：
          - 沒有定義 setter，所以 c.area = xxx 會拋出 AttributeError
          - 每次讀取都重新計算，適合「計算成本低」的場景
          - 若計算成本高，可能需要搭配快取機制
        """
        import math
        return math.pi * self.radius ** 2

    @property
    def diameter(self):
        """直徑：半徑 × 2"""
        return self.radius * 2

print("\n=== 唯讀屬性（計算值）===")
c = Circle(5)
print(f"半徑 {c.radius}，直徑 {c.diameter:.1f}，面積 {c.area:.2f}")

c.radius = 10
print(f"半徑 {c.radius}，直徑 {c.diameter:.1f}，面積 {c.area:.2f}")
# 修改 radius 後，diameter 和 area 自動更新（因為每次讀取都重新計算）

# try:
#     c.area = 100   # AttributeError：唯讀屬性不能設定

# ── 子類覆寫 setter ───────────────────────────────────────
# 研究生有加分機制，成績可以超過 100
#
# 在父類 Student 中，grade 的上限是 100。
# 現在我們想在子類 GradStudent 中放寬到 150。
#
# 使用 @Student.grade.setter 語法來「部分覆寫」setter，
# 只修改驗證邏輯，保留 getter 的行為。

class GradStudent(Student):
    """
    研究生 subclass，成績上限放寬到 150。
    
    覆寫 setter 的語法：
      @父類別.屬性名.setter
      這會建立一個新的 setter，取代父類別的 setter。
    
    注意：
      - 不需要重新定義 getter（沿用父類別的）
      - 儲存用的 _grade 屬性在父類別中已經定義
      - 這個設定在 __init__ 中同樣有效，因為 self.grade = xxx 會觸發 setter
    """

    @Student.grade.setter
    def grade(self, value):
        """
        研究生的成績 setter：放寬上限到 150。
        
        覆寫了 Student.grade 的 setter，
        但 getter 仍然沿用 Student 的版本（@property 沒有被覆寫）。
        
        參數：
            value : int — 成績（0~150 合法）
        """
        if not (0 <= value <= 150):
            raise ValueError(f"研究生成績必須在 0～150，你給了 {value}")
        self._grade = value

print("\n=== 子類覆寫 setter ===")
g = GradStudent("張教授", 120)
print(g.grade)   # 120（研究生可以超過 100）

# 記憶重點 ──────────────────────────────────────────────────
# @property           → getter，讀取時觸發
# @屬性名.setter      → setter，設定時觸發（可加驗證）
# 沒有 setter 的就是「唯讀屬性」
# 實際資料習慣存在 _屬性名（底線開頭）
#
# 進階補充：
#
#   1. @property 的底層機制是 descriptor protocol：
#      property 實作了 __get__、__set__、__delete__ 方法，
#      當屬性被存取時，Python 會優先查找 descriptor。
#
#   2. @property 也可以用來做「延遲初始化」（lazy initialization）：
#      @property
#      def data(self):
#          if not hasattr(self, '_data'):
#              self._data = expensive_computation()
#          return self._data
#      第一次存取時計算，之後回傳快取結果。
#
#   3. @property 的替代方案：
#      - __getattr__ / __setattr__：更低階的屬性存取控制
#      - descriptor class：可重複使用的屬性行為封裝
#      - dataclasses.field：搭配 __post_init__ 做驗證
#
#   4. getter 不應該有副作用（side effect）。
#      使用者預期 s.grade 只是讀取值，不會改變狀態。
#
#   5. 注意 property 的裝飾順序：
#      @property      → 建立 getter
#      @grade.setter  → 在 getter 的 property 物件上加 setter
#      @grade.deleter → 在 getter 的 property 物件上加 deleter
#      順序不能錯，一定要先有 @property 才能用 @grade.setter。
