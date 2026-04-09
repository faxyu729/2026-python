# U06. 時區操作最佳實踐：UTC 優先（3.16）
# 本程式展示為什麼應該在 UTC 中進行所有時間計算
# 問題：本地時間有夏令時跳躍問題，會導致計算錯誤
# 解決：內部計算一律使用 UTC，輸入輸出時才轉換本地時間

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 設定時區物件
utc = ZoneInfo("UTC")  # 協調世界時（無夏令時）
central = ZoneInfo("America/Chicago")  # 美國中部時區（有夏令時）

# ── 問題：本地時間計算遇到夏令時邊界（3.16）──────────
# 夏令時 (DST, Daylight Saving Time)：為節省能源，將時鐘往前撥一小時
# 美國 2013-03-10 凌晨 2:00 時鐘往前撥到 3:00
# 這意味著 2:00-3:00 之間的時間「不存在」

local_dt = datetime(2013, 3, 10, 1, 45, tzinfo=central)
# 1:45 AM CST（中部標準時間）

# ❌ 錯誤做法：直接在本地時間加減
wrong = local_dt + timedelta(minutes=30)
print(f"❌ 錯誤結果：{wrong}")  # 2:15 CST（不存在的時間！）
# 說明：1:45 + 30 分鐘 = 2:15
# 但 2:15 在夏令時跳躍時被跳過了，從 2:00 直接跳到 3:00
# 這個時間實際不存在，會導致日期時間計算錯誤

# ✓ 正確做法：先轉 UTC 計算，再轉回本地
print("\n[正確做法步驟]")
utc_dt = local_dt.astimezone(utc)
# astimezone(tz)：將時間轉換到指定時區
# 1:45 AM CST = 7:45 AM UTC（美國中部比 UTC 晚 6 小時）
print(f"轉換後 UTC：{utc_dt}")

correct = utc_dt + timedelta(minutes=30)
# 在 UTC 中計算：7:45 + 30 分鐘 = 8:15 UTC
# UTC 中沒有夏令時，計算結果完全正確
print(f"UTC 中計算結果：{correct}")

result = correct.astimezone(central)
# 8:15 UTC 轉回 CST（中部夏令時 CDT）：8:15 - 5 小時 = 3:15 CDT
print(f"✓ 正確結果：{result}")  # 3:15 CDT（正確跳過了 2:xx 時段）


# ── 最佳實踐：輸入→UTC→計算→輸出（3.16）─────────────
# 推薦的工作流程：
# 1. 輸入時：從使用者輸入或外部系統接收本地時間
# 2. 轉換：立即轉換為 UTC
# 3. 儲存：在資料庫中儲存 UTC 時間
# 4. 計算：所有業務邏輯使用 UTC 時間
# 5. 輸出：只在顯示給使用者時轉換為本地時間

print("\n[完整工作流程示例]")

# 步驟 1：使用者輸入（假設使用者在美國中部時區）
user_input = "2012-12-21 09:30:00"
print(f"使用者輸入：{user_input}（美國中部時間）")

# 步驟 2a：解析字串為 naive datetime（沒有時區資訊）
naive = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
# naive：2012-12-21 09:30:00（不知道是哪個時區）

# 步驟 2b：假設使用者在本地時區，加上時區資訊
local = naive.replace(tzinfo=central)
# local：2012-12-21 09:30:00 CST

# 步驟 2c：轉換為 UTC 進行儲存和計算
aware = local.astimezone(utc)
# 計算：09:30 CST = 15:30 UTC（美國中部冬季比 UTC 晚 6 小時）
print(f"轉換為 UTC 儲存：{aware}")

# 步驟 3-4：在系統內部操作（使用 UTC）
# 假設需要進行日期計算、排程等操作
print(f"系統內部使用 UTC：{aware}")

# 步驟 5：輸出時轉換為其他時區
taipei = ZoneInfo("Asia/Taipei")  # 台灣時區
print(f"顯示給台北用戶：{aware.astimezone(taipei)}")
# 15:30 UTC = 23:30 台灣時間（台灣比 UTC 快 8 小時）

# 補充說明
print("\n[時區轉換參考]")
print(f"UTC 時間：{aware}")
print(f"美國中部時間：{aware.astimezone(central)}")
print(f"台灣時間：{aware.astimezone(taipei)}")

# 最佳實踐要點：
# 1. ✓ 所有時間計算在 UTC 中進行
# 2. ✓ 資料庫只儲存 UTC 時間
# 3. ✓ 只在展示給使用者時才轉換本地時區
# 4. ✓ 避免在本地時間中做加減運算
# 5. ✓ 使用 ZoneInfo（Python 3.9+）或 pytz
