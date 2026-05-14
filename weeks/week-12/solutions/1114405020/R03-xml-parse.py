# R03. XML 解析基礎（6.3）
# 本檔示範 xml.etree.ElementTree 的常見讀取方式：find、findall、get、text、iter。
# 版本重點：用步驟化註解說明每一步在做什麼、為什麼做、做完會得到什麼。

import xml.etree.ElementTree as ET

# ── 步驟 0：準備 XML 測試資料 ────────────────────────────
# 目的：先建立一份可解析的 XML 文字，方便後續示範各種查找方式。
# 作法：用多行字串定義一個簡化版 RSS 結構（rss -> channel -> item）。
# 結果：xml_data 是原始字串，尚未被解析成樹狀物件。
xml_data = """
<rss version="2.0">
  <channel>
    <title>Planet Python</title>
    <item>
      <title>討論 Python 型別提示</title>
      <link>https://example.com/1</link>
      <author>Alice</author>
    </item>
    <item>
      <title>asyncio 最佳實踐</title>
      <link>https://example.com/2</link>
      <author>Bob</author>
    </item>
  </channel>
</rss>
"""

# ── 步驟 1：把 XML 字串解析成根節點 ─────────────────────
# 目的：把純文字 XML 轉成可操作的 Element 物件。
# 作法：使用 ET.fromstring(xml_data)。
# 結果：得到 root，後續可從 root 往下查詢節點與屬性。
root = ET.fromstring(xml_data)
# Step 1-1：觀察根節點資訊
# root.tag 代表目前節點名稱，root.attrib 則是屬性字典。
print("根標籤：", root.tag)           # rss
print("屬性：",   root.attrib)        # {'version': '2.0'}

# ── 步驟 2：使用 find / findall 查詢節點 ─────────────────
# 目的：學會找單一節點與多個節點。
# 作法：find() 取第一個符合節點；findall() 取全部符合節點。
# 結果：可讀出頻道名稱，並列出所有文章項目。

# Step 2-1：先找出 channel 節點
# 路徑 "channel" 代表從 root 往下一層找 <channel>。
channel = root.find("channel")
# Step 2-2：從 channel 取 title 的文字內容
# .text 代表節點內文字，例如 <title>Planet Python</title> 會得到 Planet Python。
print("頻道名稱：", channel.find("title").text)

# Step 2-3：列出所有 item
# root.findall("channel/item") 會回傳 channel 底下所有 item 節點清單。
for item in root.findall("channel/item"):
    title  = item.find("title").text
    author = item.find("author").text
  # 把每篇文章的作者與標題抓出來，整理成易讀格式。
    print(f"  [{author}] {title}")

# ── 步驟 3：使用 iter 做全域搜尋 ────────────────────────
# 目的：跨層級找出所有同名標籤。
# 作法：root.iter("title") 會遞迴遍歷整棵樹。
# 結果：不只文章 title，連頻道 title 也會被列出。
print("\n所有 <title>：")
for elem in root.iter("title"):
    print(" ", elem.text)

# ── 步驟 4：若資料來自檔案時的解析方式 ─────────────────
# 目的：了解字串解析與檔案解析的差異。
# 作法：用 ET.parse("data.xml") 讀檔，再用 getroot() 取得根節點。
# 結果：後續 find/findall/iter 的寫法都與本範例一致。
# tree = ET.parse("data.xml")
# root = tree.getroot()

# ── 步驟 5：讀取節點屬性（get）──────────────────────────
# 目的：安全取得節點屬性值。
# 作法：root.get("version") 讀取既有屬性；root.get("missing", "預設值") 示範缺值預設。
# 結果：存在的屬性回傳實值，不存在時回傳你設定的預設值，不會拋錯。
version = root.get("version")
print("\nRSS 版本：", version)        # 2.0
# Step 5-1：示範不存在屬性的安全讀取。
print("不存在的屬性：", root.get("missing", "預設值"))

# 補充：學習順序建議
# 1. 先掌握 fromstring + root.tag/root.attrib
# 2. 再練習 find/findall 與 .text 的讀取
# 3. 最後練習 iter 與 get 的全域查詢和安全取值
