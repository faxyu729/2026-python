# R08. 日期範圍與字串轉換（3.14–3.15）
# calendar.monthrange / strptime / strftime

from datetime import datetime, date, timedelta
from calendar import monthrange


# ── 3.14 當月日期範圍 ─────────────────────────────────
def get_month_range(start: date | None = None) -> tuple[date, date]:
    # 若沒有提供起始日期，預設使用「今天所在月份的第一天」。
    # replace(day=1) 只改日，不改年與月。
    if start is None:
        start = date.today().replace(day=1)
    # monthrange(year, month) 回傳 (該月第一天是星期幾, 該月總天數)。
    # 這裡只需要總天數，所以第一個值用 _ 忽略。
    _, days = monthrange(start.year, start.month)
    # 回傳 [月初, 下個月月初) 的半開區間：
    # 1. start 是本月第一天
    # 2. start + days 是「下個月第一天」
    # 這種設計在做迭代與區間判斷時較不容易出錯。
    return start, start + timedelta(days=days)


first, last = get_month_range(date(2012, 8, 1))
# 因為 last 是下個月月初，所以示範輸出時要減一天，才是本月最後一天。
print(first, "~", last - timedelta(days=1))  # 2012-08-01 ~ 2012-08-31


# 通用日期迭代生成器
def date_range(start: datetime, stop: datetime, step: timedelta):
    # 持續產生 [start, stop) 區間內的時間點，步長由 step 控制。
    # 使用 yield 可逐筆輸出，適合大範圍資料，避免一次建立整個清單。
    while start < stop:
        yield start
        # 每輪向前推進固定步長。
        start += step


# 從 2012-09-01 00:00 到 2012-09-02 00:00，每 6 小時取一個時間點。
for d in date_range(datetime(2012, 9, 1), datetime(2012, 9, 2), timedelta(hours=6)):
    print(d)
# 2012-09-01 00:00:00 / 06:00 / 12:00 / 18:00

# ── 3.15 字串轉換為日期 ───────────────────────────────
text = "2012-09-20"
# strptime: 依照格式字串把文字解析為 datetime。
# %Y=四位數年份、%m=兩位數月份、%d=兩位數日期。
dt = datetime.strptime(text, "%Y-%m-%d")
print(dt)  # 2012-09-20 00:00:00
# strftime: 把 datetime 轉成指定格式的字串。
# %A=星期全名、%B=月份全名。
print(datetime.strftime(dt, "%A %B %d, %Y"))  # 'Thursday September 20, 2012'


# 手動解析（比 strptime 快 7 倍）
def parse_ymd(s: str) -> datetime:
    # 假設輸入固定為 YYYY-MM-DD，直接 split 再轉 int。
    # 這種方式效能通常較好，但彈性與容錯性較低。
    y, m, d = s.split("-")
    return datetime(int(y), int(m), int(d))


print(parse_ymd("2012-09-20"))  # 2012-09-20 00:00:00
