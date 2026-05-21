# A02. with 語句與 Context Manager
# 「借東西要還」——確保資源一定會被釋放，就算程式出錯也一樣
# 對應 Bloom's Taxonomy：應用（Apply）— 能設計並使用自訂的 with 區塊

# ── 為什麼需要 with？ ─────────────────────────────────────
# 沒有 with 的開檔方式：如果中途發生例外，close() 可能永遠不會被呼叫
#
# Context Manager（上下文管理器）的核心精神：
#   有些資源需要「配對操作」—— 借了要還、開了要關、鎖了要解。
#   如果程式在某個操作的中間拋出例外，可能導致資源永遠無法歸還。
#
# with 語句保證了：
#   無論 with 區塊內的程式碼是正常結束還是拋出例外，
#   離開 with 區塊時，一定會執行 Context Manager 的 __exit__ 方法。

# 不好的寫法
# f = open("demo.txt", "w")
# f.write("hello")
# f.close()   # 如果 write 出錯，這行就不會執行了

# 正確的寫法：with 會自動呼叫 close()，即使出錯也一樣
# open() 本身就是一個 Context Manager，會在離開 with 時自動關閉檔案。
# 這就是最常見的 Context Manager 應用案例。
print("=== with 開檔：自動關閉 ===")
with open("/tmp/week13_demo.txt", "w") as f:
    f.write("Hello from Week 13\n")

with open("/tmp/week13_demo.txt", "r") as f:
    print(f.read().strip())

# ── 自己寫 Context Manager（用 class）────────────────────
# 需要實作兩個方法：
#   __enter__：進入 with 區塊時執行，回傳值會被 as 接收
#   __exit__ ：離開 with 區塊時執行（不管有沒有出錯）
#
# __exit__ 的三個參數：
#   exc_type : 例外型別（如果沒有例外，就是 None）
#   exc_val  : 例外實例
#   exc_tb   : 例外 traceback
#
# __exit__ 的回傳值：
#   True  → 吃掉這個例外（不讓它繼續往外傳播）
#   False → 讓例外繼續往外傳（預設行為）

import time

class Timer:
    """
    計時器 Context Manager。
    
    用法：
        with Timer() as t:
            # 這裡的程式碼會被計時
            do_something()
    
    進入 with 時記錄開始時間，離開時計算並印出經過時間。
    這個實作展示 __enter__ 可以回傳 self，
    讓外部可以透過 t 存取 Timer 實例的屬性（如 t.start）。
    """

    def __enter__(self):
        """
        進入 with 區塊時執行。
        
        在這裡記錄開始時間，並回傳 self（會被 with ... as t 的 t 接收）。
        回傳的物件不一定只能是 self，可以是任何值，
        例如 open() 回傳的是檔案物件（file object）。
        """
        self.start = time.time()
        print("⏱  開始計時")
        return self   # 這個值會被 as 接收，例如 as t

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        離開 with 區塊時執行。
        
        無論是正常離開還是發生例外，這個方法都一定會被呼叫。
        
        參數：
            exc_type : type   — 例外的型別（如 ValueError, TypeError）
            exc_val  : object — 例外實例（可用 str() 取得錯誤訊息）
            exc_tb   : object — traceback 物件（用於 debug）
        
        如果 with 區塊正常結束（無例外），三個參數都是 None。
        
        回傳值：
            False — 不吃掉例外，讓它繼續傳播（一般情況都這樣做）
            True  — 吃掉例外，程式繼續執行（很少使用）
        """
        elapsed = time.time() - self.start
        print(f"⏱  結束：{elapsed:.4f} 秒")
        return False  # False = 不吃掉例外（讓錯誤繼續往外傳）

print("\n=== 自訂計時器 ===")
with Timer() as t:
    # 計算 1 到 999999 的總和（百萬級資料量）
    total = sum(range(1_000_000))
print(f"計算結果：{total}")

# ── 更簡單的寫法：@contextmanager ─────────────────────────
# 不用寫 class，用 yield 分隔「進入前」和「離開後」
#
# contextlib.contextmanager 是一個 decorator，
# 它可以將一個「生成器函數」（有 yield 的函數）變成 Context Manager。
#
# 程式碼的執行順序：
#   1. with section("標題") → 執行 yield 之前的程式碼
#   2. yield                  → 暫停，執行 with 區塊內的程式碼
#   3. with 區塊結束         → 從 yield 之後繼續執行
#
# 這種寫法比 class 更簡潔，適用於不需要複雜 __exit__ 的場景。

from contextlib import contextmanager

@contextmanager
def section(title):
    """
    印出有邊框的區段標題。
    
    使用 @contextmanager decorator，讓一個生成器函數變成 Context Manager。
    
    執行流程：
      1. yield 之前：印出上框線與標題（進入 with 時執行）
      2. yield      ：with 區塊內的程式碼在此執行
      3. yield 之後：印出下框線（離開 with 時執行）
    
    如果 with 區塊內發生例外，yield 那一行會拋出例外，
    但因為我們沒有用 try/except 包住 yield，例外會直接傳播出去。
    """
    print(f"\n{'='*40}")
    print(f"  {title}")
    print(f"{'='*40}")
    yield           # ← with 區塊的程式碼在這裡執行
    print(f"{'─'*40}")

print()
with section("Week 13 CPE 模擬考"):
    print("  題目：UVA 11005 Cheapest Base")
    print("  時間限制：20 分鐘")

# ── CPE 應用：截取 stdout，方便測試輸出 ─────────────────
# 有些 CPE 題目會直接 print 答案
# 測試時可以截取 print 的輸出來比對
#
# 原理：
#   1. sys.stdout 是 print 的輸出目標（預設為 console）
#   2. 把 sys.stdout 換成一個 StringIO 物件，print 就會寫入記憶體
#   3. 離開 with 時，還原回原本的 sys.stdout
#
# 這個技巧在撰寫單元測試時非常有用，
# 可以直接抓取程式的輸出內容，用 assertEqual 來比對。

import io, sys

@contextmanager
def capture_output():
    """
    暫時把 print 的輸出截取到字串裡。
    
    用法：
        with capture_output() as buf:
            print("這段文字會被截取")
        
        captured = buf.getvalue()   # 取得截取的內容
    
    實作細節：
      1. 先備份舊的 sys.stdout
      2. 將 sys.stdout 指向新的 StringIO 物件
      3. yield 讓外部程式碼執行（並回傳 StringIO 物件以便讀取值）
      4. finally 區塊保證無論如何都會還原 sys.stdout
         （即使在截取期間發生了例外）
    """
    old_stdout = sys.stdout          # 備份原始的 stdout
    sys.stdout = buffer = io.StringIO()  # 將 stdout 改為 StringIO
    try:
        yield buffer     # with ... as buf 的 buf 就是這個 buffer
    finally:
        sys.stdout = old_stdout   # 一定要還原，finally 保證執行

def solve_parity(n):
    """
    UVA 10931 Parity：計算 n 的二進位裡有幾個 1。
    
    題目要求輸出格式：
      "The parity of {binary} is {count} (mod 2 is {count % 2})."
    
    範例：
      solve_parity(10) → "The parity of 1010 is 2 (mod 2 is 0)."
      solve_parity(7)  → "The parity of 111 is 3 (mod 2 is 1)."
    """
    bits = bin(n)[2:]       # bin(10) → "0b1010"，去掉 "0b" 取後半
    ones = bits.count('1')  # 計算 '1' 的個數
    print(f"The parity of {bits} is {ones} (mod 2 is {ones % 2}).")

print("\n=== 截取輸出（測試用）===")
with capture_output() as out:
    solve_parity(10)
    solve_parity(7)

captured = out.getvalue()
print("截取到的輸出：")
print(captured)

# 可以直接拿來做 assertEqual
lines = captured.strip().split('\n')
print(f"共 {len(lines)} 行輸出")

# 記憶重點 ──────────────────────────────────────────────────
# __enter__ → 進入 with 時執行，回傳值被 as 接收
# __exit__  → 離開 with 時執行（出錯也會執行）
# @contextmanager + yield → 更簡單的寫法，yield 前是 enter，yield 後是 exit
# 常用場景：開檔、計時、測試輸出截取、任何「借了要還」的資源
#
# 進階補充：
#   1. Context Manager 可以用在「分組」操作，
#      例如資料庫交易（BEGIN → COMMIT / ROLLBACK）。
#   2. 可以同時使用多個 with：
#      with open(...) as f, open(...) as g:
#   3. contextlib 還提供了 closing(), suppress(), redirect_stdout() 等工具。
#   4. @contextmanager 搭配 try/except/finally 可以處理例外，
#      在 yield 前後加上 try...except 就能決定是否要吃下特定例外。
