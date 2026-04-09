# U05. 日期時間的陷阱（3.12–3.15）
# 本程式展示日期時間處理的常見陷阱：
# 1. timedelta 不支援月份 / 2. strptime 效能問題

import timeit
import calendar
from datetime import datetime, timedelta

# ── timedelta 不支援月份（3.12）──────────────────────
# 問題：timedelta 只支援天、秒、微秒等固定時間單位
#      不支援月份和年份，因為它們長度不固定（28-31 天）
# 例如：不知道是否應該加 28、29、30 還是 31 天

dt = datetime(2012, 9, 23)

# ❌ 錯誤做法：直接使用 months 參數
try:
    result = dt + timedelta(months=1)  # type: ignore[call-arg]
except TypeError as e:
    # 會拋出：TypeError: 'months' is an invalid keyword argument for this function
    print(f"TypeError: {e}")  # 'months' is an invalid keyword argument


# ✓ 正確做法：用 calendar 取得目標月份天數，並將日期 clamp 到該月最後一天
def add_one_month(dt: datetime) -> datetime:
    # 計算目標的年與月
    year = dt.year
    month = dt.month + 1
    if month == 13:
        # 若月份超過 12，進位到下一年
        year += 1
        month = 1

    # calendar.monthrange(year, month) 傳回 (weekday, days)
    # weekday：該月 1 日的星期幾（0=Monday）
    # days：該月的天數（28-31）
    _, days_in_target_month = calendar.monthrange(year, month)

    # 把日期限制在該月最後一天
    # 例如：1 月 31 日 + 1 個月 = 2 月 29 日（不是 2 月 31 日）
    day = min(dt.day, days_in_target_month)

    return dt.replace(year=year, month=month, day=day)
    # dt.replace()：建立新的 datetime，只改變指定的欄位


print(add_one_month(datetime(2012, 1, 31)))  # 2012-02-29（1 月 31 日→2 月 29 日）
print(add_one_month(datetime(2012, 9, 23)))  # 2012-10-23（正常情況）


# ── strptime 效能問題（3.15）─────────────────────────
# 問題：datetime.strptime() 功能強大但效能較差
#      因為每次呼叫都需要解析格式字串和正則表達式編譯
# 解決：若已知確切的日期格式，可用字串分割和直接轉換更快

# 建立測試資料：2012 年所有月份的前 28 天
dates = [f"2012-{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, 29)]
# 格式："2012-01-01", "2012-01-02", ..., "2012-12-28"
# 共 12 * 28 = 336 個日期字串


def use_strptime(s: str) -> datetime:
    # ❌ 較慢的方法：使用 strptime
    # 每次呼叫都要：解析格式、編譯正則、執行匹配、建立物件
    return datetime.strptime(s, "%Y-%m-%d")
    # "%Y" = 4 位年份
    # "%m" = 2 位月份（01-12）
    # "%d" = 2 位日期（01-31）


def use_manual(s: str) -> datetime:
    # ✓ 更快的方法：手動解析（當格式確定時）
    y, m, d = s.split("-")  # 分割字串
    return datetime(int(y), int(m), int(d))  # 直接建立 datetime 物件
    # 優點：跳過格式解析和正則表達式步驟


# 驗證兩種方法結果相同
assert use_strptime("2012-09-20") == use_manual("2012-09-20")

# 效能測試：比較兩種方法
t1 = timeit.timeit(lambda: [use_strptime(d) for d in dates], number=100)
# 用 strptime 解析所有日期，執行 100 次
t2 = timeit.timeit(lambda: [use_manual(d) for d in dates], number=100)
# 用手動解析所有日期，執行 100 次

print(f"strptime: {t1:.3f}s  手動解析: {t2:.3f}s（快 {t1 / t2:.1f} 倍）")
# 手動解析通常快 5-10 倍，因為避免了格式字串的解析成本
#
# 何時使用：
#   - strptime：格式複雜或不確定時（時區、名稱月份等）
#   - 手動解析：格式簡單且確定時（ISO 日期、固定格式）
