# R03. 繼承與 super()（8.7）
# 主題：繼承 / 方法覆寫 / super() / isinstance / issubclass / 多型
# 版本重點：以步驟化註解拆解每一步，方便教學與逐行理解。

# ── 步驟 0：建立基底類別 Animal ─────────────────────────
# 目的：定義所有動物的共同屬性與共同介面。
# 作法：在基底類別中放 name 與 speak() 預設行為。
# 結果：子類別可直接繼承，必要時再覆寫。
class Animal:
    # 子步驟 0-1：初始化共同屬性 name。
    def __init__(self, name):
        self.name = name

    # 子步驟 0-2：定義共同方法 speak()（預設版）。
    def speak(self):
        return f"{self.name} 發出聲音"

    # 子步驟 0-3：定義 __repr__，讓除錯輸出更清楚。
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"


# ── 步驟 1：建立子類別並覆寫方法 ─────────────────────────
# 目的：讓不同動物有不同叫聲。
# 作法：Dog、Cat 繼承 Animal，並覆寫 speak()。
# 結果：同名方法在不同子類別可有不同實作。
class Dog(Animal):
    # 子步驟 1-1：Dog 覆寫 speak()。
    def speak(self):
        return f"{self.name} 說：汪汪！"


class Cat(Animal):
    # 子步驟 1-2：Cat 覆寫 speak()。
    def speak(self):
        return f"{self.name} 說：喵～"


# ── 步驟 2：使用 super() 延伸父類別行為 ─────────────────
# 目的：在繼承下重用父類別邏輯，避免重複程式碼。
# 作法：GuideDog 繼承 Dog，初始化時呼叫 super().__init__，
#      並在 speak() 中先取父類別結果再追加導盲犬資訊。
# 結果：保留 Dog 原本叫聲，同時增加新功能。
class GuideDog(Dog):
    # 子步驟 2-1：初始化時先呼叫父類別 __init__ 設定 name。
    # 再補上 GuideDog 專屬屬性 owner。
    def __init__(self, name, owner):
        super().__init__(name)      # 呼叫 Dog → Animal 的 __init__
        self.owner = owner

    # 子步驟 2-2：先呼叫父類別 speak() 取得基礎內容，再擴充。
    def speak(self):
        base = super().speak()      # 呼叫 Dog.speak()
        return f"{base}（導盲犬，主人：{self.owner}）"


# ── 步驟 3：建立物件並觀察覆寫與 super() 結果 ───────────
# 目的：實際驗證不同類別的 speak() 輸出差異。
# 子步驟 3-1：建立 Dog、Cat、GuideDog 三種物件。
d = Dog("小黑")
c = Cat("咪咪")
g = GuideDog("阿金", "王伯伯")

# 子步驟 3-2：逐一呼叫 speak()。
# 觀察：同一個方法名稱，會依物件真實型別執行對應版本。
for animal in [d, c, g]:
    print(animal.speak())

# ── 步驟 4：型別關係檢查（isinstance / issubclass）────────
# 目的：確認物件與類別之間的繼承關係判斷。
# 作法：
# - isinstance(obj, Class)：看物件是否是某類別或其子類別實例
# - issubclass(Sub, Base)：看類別是否繼承自另一類別
# 結果：可以安全做型別分支與 API 保護。
print(isinstance(d, Dog))       # True
print(isinstance(d, Animal))    # True（Dog 是 Animal 的子類別）
print(isinstance(d, Cat))       # False

print(issubclass(Dog, Animal))  # True
print(issubclass(Cat, Dog))     # False

# ── 步驟 5：多型（Polymorphism）示範 ───────────────────
# 目的：同一段程式碼可處理不同子類別物件。
# 作法：函式只要求物件有 speak()，不關心其具體型別。
# 結果：新增新動物類別時，通常不必修改 make_sounds()。
def make_sounds(animals: list):
    # 子步驟 5-1：逐一處理集合中的物件。
    for a in animals:
        # 子步驟 5-2：動態繫結呼叫 speak()。
        print(a.speak())        # 各自呼叫自己的 speak()

make_sounds([d, c, g])

# 學習路徑建議：
# 1. 先掌握「基底類別提供共通介面」
# 2. 再練習子類別覆寫與 super() 重用父類別邏輯
# 3. 最後理解 isinstance/issubclass 與多型在實務設計的價值
