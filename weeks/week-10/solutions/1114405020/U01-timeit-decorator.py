# U01. 計時裝飾器實作與資料格式速度比較（6.1 / 6.2 / 6.3）
# 從「重複的計時程式碼」出發，引入裝飾器，再做格式實驗
#
# 學習目標：
# 1) 看懂為什麼「橫切邏輯」（例如計時、記錄 log）適合用裝飾器
# 2) 了解 functools.wraps 的作用（保留被包裝函式的原始資訊）
# 3) 用同一批資料比較 CSV / JSON / XML 解析速度，建立效能直覺

import csv
import json
import time
import io
import xml.etree.ElementTree as ET
import functools

# ═══════════════════════════════════════════════════════════
# Part 1｜問題：每個函式都要手動計時 → 大量重複
# ═══════════════════════════════════════════════════════════

def read_csv_raw(data: str) -> list:
    """把 CSV 文字解析成 list[dict]。

    參數:
        data: CSV 格式字串，第一列需包含欄位名稱。
    回傳:
        每列一個 dict（值皆為字串）。
    """
    return list(csv.DictReader(io.StringIO(data)))

def read_json_raw(data: str) -> list:
    """把 JSON 文字解析成 Python 物件（此例為 list[dict]）。"""
    return json.loads(data)

def read_xml_raw(data: str) -> list:
    """把 XML 文字解析成 list[dict]。

    本例的 XML 每筆資料長相為：
        <row id="..." name="..." score="..."/>
    因此直接讀取 row.attrib 即可拿到屬性字典。
    """
    root = ET.fromstring(data)
    return [r.attrib for r in root.findall("row")]

# 沒有裝飾器：每次都要複製貼上計時程式碼 ↓
# start = time.perf_counter()
# result = read_csv_raw(data)
# print(f"read_csv_raw 耗時 {time.perf_counter() - start:.6f}s")
#
# start = time.perf_counter()
# result = read_json_raw(data)
# print(f"read_json_raw 耗時 {time.perf_counter() - start:.6f}s")
# ... 每加一個函式就多寫三行，且容易忘記移除

# ═══════════════════════════════════════════════════════════
# Part 2｜解法：裝飾器把計時邏輯包起來，一次定義，到處復用
# ═══════════════════════════════════════════════════════════

def timeit(func):
    """基礎版計時裝飾器。

    這個函式接收「被裝飾的函式 func」，回傳新的 wrapper：
    - 呼叫 wrapper 時先記錄開始時間
    - 再呼叫原本的 func
    - 最後印出耗時並回傳 func 的結果
    """
    def wrapper(*args, **kwargs):
        # perf_counter 解析度高，適合做短時間區間測量。
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        # <20s 為左對齊固定寬度，讓多行輸出更整齊。
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        return result
    return wrapper

# 問題：wrapper 蓋掉了原函式的 __name__ / __doc__
def demo():
    """這是 demo 的說明文字"""
    pass

wrapped = timeit(demo)
print("未加 wraps 前：", wrapped.__name__)   # wrapper（錯誤！）

# ── Part 3｜functools.wraps：保留原函式的 metadata ──────────

def timeit(func):
    """改良版計時裝飾器：使用 functools.wraps 保留原函式資訊。"""
    @functools.wraps(func)          # 保留 __name__ / __doc__ / __module__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        return result
    return wrapper

wrapped = timeit(demo)
print("加 wraps 後：  ", wrapped.__name__)   # demo（正確）
print()

# ═══════════════════════════════════════════════════════════
# Part 4｜實驗：相同資料，CSV vs JSON vs XML 速度比較
# ═══════════════════════════════════════════════════════════

# ── 產生測試資料（1000 筆學生記錄）────────────────────────
# 固定資料量可讓不同格式比較更公平，也方便重現結果。
N = 1000

# CSV 格式
csv_buf = io.StringIO()
# DictWriter 以欄位名控制輸出順序，避免欄位順序不一致。
writer = csv.DictWriter(csv_buf, fieldnames=["id", "name", "score"])
writer.writeheader()
for i in range(N):
    # score 以循環方式落在 60~99，避免單調資料太過理想化。
    writer.writerow({"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40})
# getvalue() 取出完整 CSV 文字，供後續測速使用。
CSV_DATA = csv_buf.getvalue()

# JSON 格式
# JSON 直接序列化 list[dict]，是常見 API 傳輸格式。
JSON_DATA = json.dumps([
    {"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40}
    for i in range(N)
])

# XML 格式
# 這裡用字串拼接快速產生測試資料，實務上可用 ElementTree 建構。
xml_rows = "".join(
    f'<row id="{i}" name="Student{i:04d}" score="{60 + i % 40}"/>'
    for i in range(N)
)
XML_DATA = f"<data>{xml_rows}</data>"

# ── 帶回傳耗時的計時包裝 ─────────────────────────────────

def timeit_silent(func):
    """回傳 (原結果, 耗時) 的計時裝飾器，不在函式內直接列印。

    為什麼需要 silent 版本：
    - 若每次迴圈都 print，I/O 成本會干擾測速結果
    - 把耗時回傳後，可在外層集中統計平均值
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        return result, time.perf_counter() - start
    return wrapper

_csv  = timeit_silent(read_csv_raw)
_json = timeit_silent(read_json_raw)
_xml  = timeit_silent(read_xml_raw)

# ── 執行比較（重複 5 次取平均，排除冷啟動影響）────────────

RUNS = 5
# 使用 dict 累加總時間，最後除以 RUNS 算平均。
times = {"CSV": 0.0, "JSON": 0.0, "XML": 0.0}

for _ in range(RUNS):
    # 這裡刻意忽略解析結果內容（以 _ 接收），只關注耗時。
    _, t = _csv(CSV_DATA);   times["CSV"]  += t
    _, t = _json(JSON_DATA); times["JSON"] += t
    _, t = _xml(XML_DATA);   times["XML"]  += t

print(f"=== 讀取 {N} 筆資料，重複 {RUNS} 次平均 ===\n")
print(f"{'格式':<6} {'平均耗時':>12}  {'相對 JSON':>10}")
# 以 JSON 作為基準（1.00x），其餘格式顯示相對倍數。
base = times["JSON"] / RUNS
for fmt, total in times.items():
    avg = total / RUNS
    print(f"  {fmt:<6} {avg:.6f}s   {avg/base:>8.2f}x")

# ═══════════════════════════════════════════════════════════
# 觀察重點
# ═══════════════════════════════════════════════════════════
# 1. JSON 通常最快（原生 C 實作的解析器）
# 2. XML  通常最慢（文字解析開銷大，屬性字串轉換）
# 3. CSV  介於中間（簡單格式，但每欄都是字串需自行轉型）
#
# 裝飾器帶來的好處：
# - 計時邏輯只寫一次，不汙染原函式
# - 要移除計時只需拿掉 @timeit，函式本身不需修改
# - functools.wraps 確保 debug / help() 時能看到正確名稱
# - 可延伸到記錄日誌、權限檢查、重試機制等共用需求
