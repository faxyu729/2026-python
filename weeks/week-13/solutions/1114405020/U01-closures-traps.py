# U01. 陷阱！閉包與可變預設值
# 兩個「寫起來看似正確，但結果出乎意料」的 Python 坑
# 對應 Bloom's Taxonomy：理解（Understand）— 能解釋為什麼會出錯

# ── 陷阱 1：可變的預設值 ─────────────────────────────────
# 關鍵：函數的預設值只在「定義時」建立一次，之後每次呼叫都共用同一個物件
#
# 錯誤根源：
#   Python 在執行 def 陳述式時，會將「預設值物件」建立好並附加到函數物件上。
#   → 這個預設值物件「只被建立一次」，不會每次呼叫都重新建立。
#
#   對於不可變型別（int, str, tuple, None），這沒有問題，
#   因為每次對它們的操作都會產生新的物件，不會修改到原始值。
#
#   但對於可變型別（list, dict, set），
#   在函數內對它們進行「就地修改」（如 .append(), .add(), .update()），
#   會直接修改到那個共用的預設值物件，導致下次呼叫時狀態被延續。
#
# 視覺化理解：
#   def add_to_cart(item, cart=[]):
#   → Python 記住了 cart 指向「某個特定的 list 物件 A」
#   → 第一次呼叫：對 A 做 append("蘋果")，A 變成 ["蘋果"]
#   → 第二次呼叫：對 A 做 append("香蕉")，A 變成 ["蘋果", "香蕉"]
#   → 共享同一個 A，不是每次新建立

def add_to_cart(item, cart=[]):   # ← 這個 [] 只建立一次！
    cart.append(item)
    return cart

print("=== 陷阱 1：可變預設值 ===")
print(add_to_cart("蘋果"))   # ['蘋果']
print(add_to_cart("香蕉"))   # ['蘋果', '香蕉']  ← 驚！不是 ['香蕉']
print(add_to_cart("葡萄"))   # ['蘋果', '香蕉', '葡萄']
# 原因：cart=[] 這個 list 在 def 時就建好了，三次呼叫都用同一個

print("\n--- 正確寫法：用 None 當預設值 ---")
def add_to_cart_safe(item, cart=None):
    """
    安全的購物車函數：每次呼叫都建立新的 list。
    
    關鍵：
      - 預設值使用不可變的 None（每次都是同一個 None，但 None 不能修改）
      - 在函數內部檢查 cart is None，才建立新的 list
      - 這樣每次呼叫（不傳 cart 時）都會獲得一個全新的 list
    
    這個模式（None 作為 sentinel value）在 Python 非常常見，
    是官方推薦的處理可變預設值的方式。
    """
    if cart is None:
        cart = []   # ← 每次呼叫才建立新的 list
    cart.append(item)
    return cart

print(add_to_cart_safe("蘋果"))  # ['蘋果']
print(add_to_cart_safe("香蕉"))  # ['香蕉'] ← 各自獨立，正確！

# ── 陷阱 2：閉包的延遲綁定 ───────────────────────────────
# 關鍵：閉包記住的是「變數名稱」，不是「當下的值」
# 等迴圈跑完，i 已經是最後的值了
#
# 閉包（closure）的運作機制：
#   當一個巢狀函數（如 lambda）引用了外層函數的變數時，
#   Python 不會把「當下的值」複製到巢狀函數中，
#   而是建立一個對「外層變數名稱」的參照（reference）。
#
#   等到巢狀函數真正被呼叫時，它才去查那個變數名稱現在指向什麼值。
#   如果外層的變數在迴圈中一直在變，等到迴圈結束時，
#   變數的值已經是迴圈的最終值了。
#
#   這就是為什麼 funcs 裡所有的 lambda 都回傳 4：
#   當 f() 被呼叫時，外層的 i 已經是 4（for 迴圈結束後的值）。

print("\n=== 陷阱 2：閉包延遲綁定 ===")
funcs = []
for i in range(5):
    funcs.append(lambda: i)   # ← lambda 記住「i」這個名字，不是值

print("你以為：", [0, 1, 2, 3, 4])
print("實際上：", [f() for f in funcs])  # [4, 4, 4, 4, 4]，全部都是 4！
# 原因：迴圈結束後 i=4，所有 lambda 去查 i，都查到 4

print("\n--- 正確寫法：用預設參數把值「複製」進來 ---")
funcs_ok = []
for i in range(5):
    funcs_ok.append(lambda i=i: i)   # ← i=i 把當下的值複製成預設值

print("修正後：", [f() for f in funcs_ok])  # [0, 1, 2, 3, 4] ✓
#
# 原理：
#   lambda i=i: i  中的「右邊 i」是外層的 i（當下值），
#   「左邊 i」是 lambda 的預設參數。
#   Python 在建立 lambda 時會立刻求值「右邊 i」，
#   把當下的值（0, 1, 2, 3, 4）分別固定為每個 lambda 的預設值。
#   這和陷阱 1（可變預設值）是同一機制，
#   只是在這裡，我們利用「預設值在定義時就被固定」的特性來解決閉包問題。

# ── nonlocal：在閉包裡修改外層的變數 ─────────────────────
# 閉包預設只能「讀取」外層變數
# 要修改外層變數，必須用 nonlocal 宣告
#
# Python 的作用域規則（LEGB）：
#   Local → Enclosing → Global → Built-in
#   巢狀函數可以讀取外層函數的變數（Enclosing scope），
#   但如果沒有特別宣告，賦值操作（=）會被視為在 Local scope 建立新變數。
#
# nonlocal 的宣告告訴 Python：
#   「這個變數不在本層，去外層（Enclosing scope）找它，
#    而且我要修改它的值。」
#
# 如果不寫 nonlocal：
#   count += 1  → Python 認為「建立一個區域變數 count，
#                  然後試圖讀取它的值再做 +1」
#                 → 但 count 還沒被賦值 → UnboundLocalError

print("\n=== nonlocal：修改外層變數 ===")

def make_counter(start=0):
    """
    回傳一個計數器函數，每次呼叫加 1。
    
    這個閉包的應用場景是「需要記住狀態，但又不需要整個 class」。
    每次呼叫 make_counter() 都會建立一個獨立的 count 變數，
    以及一個可以修改這個 count 的巢狀函數。
    
    參數：
        start : int — 計數器的起始值（預設 0）
    
    回傳值：
        function — 每次呼叫會 +1 並回傳新值的計數器函數
    """
    count = start

    def counter():
        nonlocal count   # ← 宣告「我要修改外層的 count，不是建新的」
        count += 1
        return count

    return counter

c1 = make_counter()
c2 = make_counter(10)
print(c1(), c1(), c1())   # 1 2 3
print(c2(), c2())         # 11 12
print(c1())               # 4（c1 和 c2 是各自獨立的計數器）
# c1 和 c2 各自有自己的 count 變數，
# 因為每次呼叫 make_counter() 都會建立新的 Enclosing scope。

# ── 實際應用：用閉包做「一次性」工具函數 ────────────────
# CPE 中偶爾需要「記住狀態」但又不想寫整個 class
#
# 閉包 vs class 的取捨：
#   閉包：適合「只有一個方法」的簡單狀態管理，程式碼更精簡
#   class：適合「有多個方法」的複雜狀態管理，可讀性與擴充性更好

print("\n=== 閉包應用：記住已走過的節點 ===")
def make_visit_tracker():
    """
    建立一個「已訪問節點追蹤器」。
    
    在圖論或樹走訪中，需要記錄哪些節點已經走過。
    用閉包封裝 visited set，不讓外部直接修改。
    
    回傳值：
        visit(node) — function
            node：要檢查的節點
            回傳 True（第一次訪問）或 False（已訪問過）
    """
    visited = set()

    def visit(node):
        nonlocal visited
        if node in visited:
            return False    # 已走過
        visited.add(node)
        return True         # 第一次走到

    return visit

visit = make_visit_tracker()
results = [visit(n) for n in [1, 2, 1, 3, 2, 4]]
print(results)  # [True, True, False, True, False, True]

# 記憶重點 ──────────────────────────────────────────────────
# 可變預設值陷阱 → 預設值用 None，函數內再建 [] 或 {}
# 閉包延遲綁定  → 用 lambda x=x: x 把值固定下來
# nonlocal      → 要「修改」外層變數時才需要，只「讀取」不用
#
# 進階補充：
#   1. 可變預設值陷阱也可以用 *args/**kwargs 來規避：
#      def add_to_cart(item, *cart):
#          cart = list(cart)  # 每次都是新的 tuple 轉 list
#          cart.append(item)
#          return cart
#
#   2. Python 的 default argument 在 def 時求值，
#      但 type hint annotation 也是在 def 時求值（可用 string literal 延遲）。
#
#   3. nonlocal 只在巢狀函數內有效，global 才是修改模組層級的變數。
#
#   4. 閉包會建立 Enclosing scope 的 cell object，
#      使得外層函數的變數不會被 GC 回收，這是閉包的記憶體成本。
