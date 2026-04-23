# R02. 路徑操作與目錄列舉（5.11 / 5.12 / 5.13）
# Bloom: Remember — 會用 pathlib 組路徑、檢查存在、列出檔案

import os
from pathlib import Path

# ── 5.11 組路徑：pathlib 是現代寫法 ────────────────────
# Path 物件可把路徑當成「可操作的物件」，
# 比單純字串串接更安全、可讀性更高。
# 使用 / 來組路徑是 pathlib 的常見寫法。
#
# 觀念補充：
# 1) Path("weeks") / "week-09" 不等於字串相加；它會建立新的 Path 物件。
# 2) 不用手動寫 "/" 或 "\\"，程式會依作業系統使用正確分隔符號。
# 3) 這種寫法可避免「多打一個斜線、少打一個斜線」的路徑錯誤。
base = Path("weeks") / "week-09"
print(base)              # 完整路徑字串表示；Windows 會顯示反斜線
print(base.name)         # 最後一層名稱（basename）
print(base.parent)       # 上一層路徑（parent directory）
print(base.suffix)       # 副檔名；資料夾通常是空字串

# 進一步理解這三個常用屬性：
# - name: 最後一段完整名稱，例如 "week-09" 或 "report.csv"
# - stem: 檔名主體，例如 "report.csv" 的 stem 是 "report"
# - suffix: 副檔名（含點），例如 ".csv"；若無副檔名則為空字串

f = Path("hello.txt")
# stem: 檔名去掉副檔名後的主體
# suffix: 包含點號的副檔名
print(f.stem, f.suffix)  # hello .txt

# 相容舊寫法：os.path.join
# 在舊程式或教學中仍常見 os.path.join，
# 它會依作業系統自動選擇適合的路徑分隔符號。
#
# 實務建議：
# - 新程式優先用 pathlib（可讀性較好，功能物件化）
# - 維護舊程式時看懂 os.path.join 仍很重要
print(os.path.join("weeks", "week-09", "README.md"))

# ── 5.12 存在判斷 ──────────────────────────────────────
p = Path("hello.txt")
# exists(): 只判斷路徑是否存在（不分檔案或資料夾）
# is_file(): 路徑存在且為檔案才會 True
# is_dir(): 路徑存在且為資料夾才會 True
#
# 判斷順序常見寫法：
# 1) 先 exists() 確認目標存在
# 2) 再用 is_file()/is_dir() 決定後續處理流程
# 這能讓錯誤訊息更清楚，也比較容易除錯。
print(p.exists())
print(p.is_file())
#process lock file
print(p.is_dir())

missing = Path("no_such_file.txt")
# 實務上常在讀檔前先做存在檢查，
# 可避免直接 open() 導致 FileNotFoundError。
# 注意：檔案有可能在「檢查後、開啟前」被刪除（競態條件）。
# 在高可靠度程式中，通常仍要搭配 try/except 做最後保護。
if not missing.exists():
    print(f"{missing} 不存在，略過讀取")

# ── 5.13 列出資料夾內容 ────────────────────────────────
here = Path(".")
# Path(".") 代表目前工作目錄（current working directory）。
# 目前工作目錄不一定等於程式檔所在目錄，
# 會受你從哪裡執行 python 影響。

# 只列當層
# os.listdir() 只回傳名稱（字串），不含完整路徑資訊。
# 若需要路徑物件，通常要再手動 here / name 組合。
for name in os.listdir(here):
    print("listdir:", name)

# 只抓 .py（當層）
# glob("*.py") 會回傳 Path 物件，
# 只比對目前資料夾，不會深入子資料夾。
# 也就是說，子資料夾裡的 .py 不會出現在這個迴圈。
for p in here.glob("*.py"):
    print("glob:", p)

# 遞迴抓所有 .py（含子資料夾）
# rglob("*.py") 會遞迴搜尋（recursive glob），
# 適合專案級掃描；檔案多時結果可能很多。
# 若專案很大，遞迴搜尋可能花時間，
# 實務上可搭配條件過濾、或限制起始目錄縮小範圍。
for p in Path("..").rglob("*.py"):
    print("rglob:", p)
    break  # 示範用途：只印第一筆，避免輸出過長
