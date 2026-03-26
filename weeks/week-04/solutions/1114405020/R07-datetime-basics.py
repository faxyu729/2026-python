# R07. 日期時間基本運算（3.12–3.13）
# timedelta 加減 / weekday() 計算指定星期

from datetime import datetime, timedelta

# ── 3.12 timedelta 基本運算 ───────────────────────────
# timedelta 用來表示「時間差」，可用 days / hours / minutes 等參數建立。
a = timedelta(days=2, hours=6)
# 4.5 小時可直接使用浮點數，等價於 4 小時 30 分鐘。
b = timedelta(hours=4.5)
# timedelta 之間可直接相加，結果仍是 timedelta。
c = a + b
# .days 只會回傳「整天」部分。
print(c.days)  # 2
# 若要看完整時數（含不足一天的部分），可用 total_seconds() 換算。
print(c.total_seconds() / 3600)  # 58.5

# datetime + timedelta 可得到未來/過去某一時刻。
dt = datetime(2012, 9, 23)
print(dt + timedelta(days=10))  # 2012-10-03 00:00:00

# 兩個 datetime 相減會得到 timedelta，可再取天數等資訊。
d1, d2 = datetime(2012, 9, 23), datetime(2012, 12, 21)
print((d2 - d1).days)  # 89

# 閏年自動處理
# datetime 的日期運算會自動考慮曆法規則，不需自行判斷閏年。
print((datetime(2012, 3, 1) - datetime(2012, 2, 28)).days)  # 2（閏年）
print((datetime(2013, 3, 1) - datetime(2013, 2, 28)).days)  # 1（平年）

# ── 3.13 計算指定星期日期 ─────────────────────────────
WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_previous_byday(dayname: str, start: datetime | None = None) -> datetime:
    # 未提供起始日就用今天，讓函式可直接獨立使用。
    if start is None:
        start = datetime.today()
    # weekday(): Monday=0 ... Sunday=6
    day_num = start.weekday()
    # 找出目標星期在 WEEKDAYS 中的索引（同樣是 0~6）。
    target = WEEKDAYS.index(dayname)
    # 使用模運算算出「要往前退幾天」：
    # 1. (7 + day_num - target) % 7 會得到 0~6
    # 2. 若結果是 0，代表同一天；題目要找 previous，所以改成 7 天前
    days_ago = (7 + day_num - target) % 7 or 7
    # 回傳上一個指定星期的日期時間。
    return start - timedelta(days=days_ago)


base = datetime(2012, 8, 28)  # 週二
# 以 2012-08-28（週二）為基準，往前找最近的週一與週五。
print(get_previous_byday("Monday", base))  # 2012-08-27
print(get_previous_byday("Friday", base))  # 2012-08-24
