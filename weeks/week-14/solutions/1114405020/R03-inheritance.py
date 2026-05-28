# R03. 繼承與 super()（8.7）
# 繼承 / 方法覆寫 / super() / isinstance / issubclass
#
# 繼承（inheritance）是物件導向程式設計的三大特性之一。
# 子類別（subclass）可以繼承父類別（superclass）的所有屬性和方法，
# 並可覆寫（override）或擴充（extend）父類別的行為。
# super() 則讓子類別可以明確呼叫父類別的版本。

# ── 基底類別 ─────────────────────────────────────────────

class Animal:
    """動物的基底類別，定義所有動物共有的行為。"""

    def __init__(self, name):
        """建構子：儲存動物名稱。
        此處 name 會被所有子類別繼承。"""
        self.name = name

    def speak(self):
        """動物叫聲的預設實作。子類別應覆寫此方法。"""
        return f"{self.name} 發出聲音"

    def __repr__(self):
        """使用 self.__class__.__name__ 動態取得目前類別名稱，
        這樣即使被子類別呼叫，也能顯示正確的類別名稱。
        {self.name!r} 中的 !r 表示使用 repr() 來呈現字串（會帶引號）。"""
        return f"{self.__class__.__name__}({self.name!r})"


# ── 子類別：覆寫方法 ──────────────────────────────────────

class Dog(Animal):
    """狗類別，繼承 Animal。示範完全覆寫（override）父類別方法。"""

    def speak(self):
        """覆寫 Animal.speak()，提供狗專屬的叫聲。"""
        return f"{self.name} 說：汪汪！"


class Cat(Animal):
    """貓類別，繼承 Animal。同樣覆寫 speak() 方法。"""

    def speak(self):
        return f"{self.name} 說：喵～"


# ── super()：呼叫父類別方法 ───────────────────────────────

class GuideDog(Dog):
    """導盲犬類別，繼承 Dog。示範使用 super() 擴充父類別方法。
    繼承鏈：GuideDog → Dog → Animal。"""

    def __init__(self, name, owner):
        """擴充建構子：先透過 super() 呼叫 Dog.__init__（進而呼叫 Animal.__init__），
        再新增導盲犬特有的 owner 屬性。
        如果跳過 super().__init__()，則父類別的初始化邏輯不會被執行。"""
        super().__init__(name)      # 沿 MRO（方法解析順序）向上呼叫
        self.owner = owner

    def speak(self):
        """擴充 speak()：先用 super().speak() 取得 Dog 版本的叫聲，
        再追加導盲犬專屬的描述文字。"""
        base = super().speak()      # 呼叫 Dog.speak() → "小黑 說：汪汪！"
        return f"{base}（導盲犬，主人：{self.owner}）"


d = Dog("小黑")          # 建立 Dog 實例
c = Cat("咪咪")          # 建立 Cat 實例
g = GuideDog("阿金", "王伯伯")  # 建立 GuideDog 實例

# 示範多型：相同的 speak() 介面，不同的實作結果
for animal in [d, c, g]:
    print(animal.speak())

# ── isinstance / issubclass ───────────────────────────────

print(isinstance(d, Dog))       # True  — d 是 Dog 的實例
print(isinstance(d, Animal))    # True  — Dog 是 Animal 的子類別，所以 d 也是 Animal 的一種
print(isinstance(d, Cat))       # False — d 和 Cat 無關

print(issubclass(Dog, Animal))  # True  — Dog 繼承自 Animal
print(issubclass(Cat, Dog))     # False — Cat 並未繼承 Dog

# ── 多型（Polymorphism）──────────────────────────────────

def make_sounds(animals: list):
    """多型（polymorphism）的典型範例：不管傳入哪種動物，
    只要該物件有 speak() 方法，即可統一呼叫。
    不需要知道物件的實際類別，只需要確認它有我們需要的介面。
    這就是「鴨子型別」（duck typing）：如果它走起來像鴨子、叫起來像鴨子，它就是鴨子。"""
    for a in animals:
        print(a.speak())        # 各自呼叫自己的 speak()，執行不同的實作

make_sounds([d, c, g])
