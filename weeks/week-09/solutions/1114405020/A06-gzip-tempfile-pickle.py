# A06. 壓縮檔、臨時資料夾、物件序列化（5.7 / 5.19 / 5.21）
# Bloom: Apply — 能把標準庫工具組合起來解一個小任務

import gzip
import pickle
import tempfile
from pathlib import Path

# ── 5.7 讀寫壓縮檔：gzip.open 幾乎和 open 一樣 ─────────
# gzip.open 的使用方式與 open 類似，差別在於：
# - 讀寫時會自動進行壓縮/解壓縮
# - 副檔名常見 .gz（慣例，不是硬性規定）
#
# 文字模式（wt/rt）處理 str，務必指定 encoding，
# 才能穩定處理中文與跨平台環境。
with gzip.open("notes.txt.gz", "wt", encoding="utf-8") as f:
    f.write("第一行筆記\n")
    f.write("第二行筆記\n")

# 讀回：直接逐行迭代
# 這裡迭代的是「解壓後的文字行」，
# 寫法和一般文字檔一致。
with gzip.open("notes.txt.gz", "rt", encoding="utf-8") as f:
    for line in f:
        print("gz:", line.rstrip())

# 也能用 'wb'/'rb' 處理二進位資料
# 二進位模式直接處理 bytes，不涉及 encoding。
# 常見於圖片、模型、封包、序列化資料等非純文字內容。
with gzip.open("blob.bin.gz", "wb") as f:
    f.write(b"\x00\x01\x02\x03")

# stat().st_size 看到的是「壓縮後檔案大小」。
# 小資料有時會因為 gzip 檔頭而不一定更小，屬正常現象。
print("blob size:", Path("blob.bin.gz").stat().st_size, "bytes")

# ── 5.19 臨時檔案與資料夾：離開 with 自動清理 ──────────
# 場景：想跑個小實驗但不想在專案亂留檔
# TemporaryDirectory() 會建立一個臨時資料夾，
# with 區塊結束時自動刪除，避免留下測試垃圾檔案。
with tempfile.TemporaryDirectory() as tmp:
    # tempfile 回傳字串路徑，轉成 Path 後操作更直覺。
    tmp = Path(tmp)
    print("暫存資料夾:", tmp)

    # 在裡面寫幾個檔
    (tmp / "a.txt").write_text("hello\n", encoding="utf-8")
    (tmp / "b.txt").write_text("world\n", encoding="utf-8")

    # 列出內容
    # iterdir() 只列當層項目，不遞迴。
    for p in tmp.iterdir():
        print("  ", p.name, "→", p.read_text(encoding="utf-8").rstrip())

# 離開 with 後，tmp 已自動刪除
# 這行可用來驗證自動清理確實發生。
print("離開後還存在嗎？", tmp.exists())  # False

# 單一臨時檔：NamedTemporaryFile
# NamedTemporaryFile 會建立「有實體檔名」的臨時檔，
# 適合需要把路徑交給其他 API/程式的情境。
# delete=False 代表離開 with 不自動刪，讓你可以在外部再使用一次。
with tempfile.NamedTemporaryFile("wt", delete=False, suffix=".log",
                                 encoding="utf-8") as f:
    f.write("暫存 log\n")
    log_path = f.name
print("暫存檔位置:", log_path)
# 因為上面設定 delete=False，所以這裡手動刪除。
Path(log_path).unlink()

# ── 5.21 pickle：把 Python 物件「原樣」存檔 ────────────
# 適用：dict/list/自訂類別；不適用：跨語言、長期存檔（用 json 更穩）
# pickle 的核心用途是「Python 內部資料快照」，
# 優點是方便、保留結構；缺點是相依 Python 生態，不易跨語言。
scores = {
    "alice": [90, 85, 92],
    "bob":   [70, 75, 80],
    "carol": [88, 91, 95],
}

# 注意：pickle 是 bytes → 一定要 'wb'/'rb'
# dump: 物件 -> 檔案（序列化）
with open("scores.pkl", "wb") as f:
    pickle.dump(scores, f)

# load: 檔案 -> 物件（反序列化）
with open("scores.pkl", "rb") as f:
    loaded = pickle.load(f)

print("讀回的物件:", loaded)
print("型別一致?", type(loaded) is dict)         # True
print("內容相等?", loaded == scores)              # True
# 額外做一個運算，確認讀回資料可直接當一般 Python 物件使用。
print("alice 平均:", sum(loaded["alice"]) / 3)   # 89.0

# ⚠️ 安全提醒：pickle.load 會執行內嵌指令，
# 絕對不要對「來路不明」的 .pkl 檔做 load。

# ── 課堂延伸挑戰 ───────────────────────────────────────
# 1) 把 scores 存成 gzip 壓縮後的 pickle：gzip.open('scores.pkl.gz','wb')
# 2) 用 TemporaryDirectory 跑完整流程（寫→讀→比對），不在專案留任何檔
# 3) 試著 pickle 一個 lambda，觀察錯誤訊息（pickle 不能存 lambda）
