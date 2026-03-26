# R09. 時區操作（3.16）
# zoneinfo（Python 3.9+）取代 pytz

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, available_timezones

# ZoneInfo 會從系統/IANA 時區資料庫載入時區規則（含夏令時間）。
# 常見做法是先準備好常用時區物件，避免重複建立。
utc = ZoneInfo("UTC")
central = ZoneInfo("America/Chicago")
taipei = ZoneInfo("Asia/Taipei")

# 建立帶時區的 datetime
# tzinfo 有設定時，datetime 會是「aware datetime」（含時區資訊）。
# aware datetime 才適合做跨時區轉換與比較。
d = datetime(2012, 12, 21, 9, 30, 0, tzinfo=central)
print(d)  # 2012-12-21 09:30:00-06:00

# 轉換時區
# astimezone() 會保持「同一個絕對時間點」，只改成目標時區表示法。
# 也就是牆上時間（幾點幾分）會改變，但實際瞬間不變。
print(d.astimezone(ZoneInfo("Asia/Kolkata")))  # 2012-12-21 21:00:00+05:30
print(d.astimezone(taipei))  # 2012-12-21 23:30:00+08:00

# 取得當前 UTC 時間
# 使用 UTC 作為系統內部標準時間，可避免跨時區與夏令時間陷阱。
now_utc = datetime.now(tz=utc)
print(now_utc)

# 最佳實踐：內部用 UTC，輸出再轉本地
# 這裡先建立 UTC 時間，再於展示層轉成美國中部時區。
# 2013-03-10 是北美切換夏令時間的日期，
# 使用 zoneinfo 可自動套用當地規則，不需手動計算偏移。
utc_dt = datetime(2013, 3, 10, 7, 45, 0, tzinfo=utc)
print(utc_dt.astimezone(central))  # 2013-03-10 01:45:00-06:00

# 查詢國家時區

# available_timezones() 會回傳可用時區名稱集合。
# 這裡用字串過濾示範找出台北相關時區。
tw_zones = [z for z in available_timezones() if "Taipei" in z]
print(tw_zones)  # ['Asia/Taipei']
