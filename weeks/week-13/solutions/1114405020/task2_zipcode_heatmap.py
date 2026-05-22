import csv
import platform
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent.parent.parent / "assets" / "stu-data"
OUTPUT_DIR = HERE / "output"

YEARS = list(range(109, 115))

_CJK_FONTS = {
    "Darwin":  ["Heiti TC", "Arial Unicode MS", "PingFang TC"],
    "Windows": ["Microsoft JhengHei", "Microsoft YaHei"],
    "Linux":   ["Noto Sans CJK TC", "WenQuanYi Zen Hei"],
}.get(platform.system(), ["sans-serif"])


def _apply_cjk_font():
    plt.rcParams["font.sans-serif"] = _CJK_FONTS + plt.rcParams["font.sans-serif"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False


ZIPCODE_TO_COUNTY = {
    "880": "澎湖縣", "881": "澎湖縣", "882": "澎湖縣", "884": "澎湖縣",
    "100": "台北市", "103": "台北市", "104": "台北市", "106": "台北市",
    "110": "台北市", "111": "台北市", "114": "台北市", "115": "台北市",
    "116": "台北市",
    "200": "基隆市", "201": "基隆市", "202": "基隆市", "203": "基隆市",
    "220": "新北市", "221": "新北市", "231": "新北市", "234": "新北市",
    "235": "新北市", "236": "新北市", "238": "新北市", "239": "新北市",
    "241": "新北市", "242": "新北市", "243": "新北市", "244": "新北市",
    "247": "新北市", "248": "新北市", "251": "新北市", "252": "新北市",
    "253": "新北市",
    "260": "宜蘭縣", "261": "宜蘭縣", "263": "宜蘭縣", "265": "宜蘭縣",
    "300": "新竹市", "302": "新竹縣", "303": "新竹縣", "304": "新竹縣",
    "305": "新竹縣", "306": "新竹縣", "307": "新竹縣", "308": "新竹縣",
    "310": "苗栗縣", "350": "苗栗縣", "351": "苗栗縣", "360": "苗栗縣",
    "400": "台中市", "401": "台中市", "402": "台中市", "403": "台中市",
    "404": "台中市", "406": "台中市", "407": "台中市", "408": "台中市",
    "411": "台中市", "412": "台中市", "413": "台中市", "420": "台中市",
    "421": "台中市", "422": "台中市", "423": "台中市", "424": "台中市",
    "426": "台中市", "427": "台中市", "428": "台中市", "429": "台中市",
    "430": "台中市", "431": "台中市", "432": "台中市", "433": "台中市",
    "434": "台中市", "435": "台中市", "436": "台中市", "437": "台中市",
    "438": "台中市", "439": "台中市",
    "500": "彰化縣", "502": "彰化縣", "503": "彰化縣", "504": "彰化縣",
    "505": "彰化縣", "506": "彰化縣", "507": "彰化縣", "508": "彰化縣",
    "509": "彰化縣", "510": "彰化縣", "511": "彰化縣", "512": "彰化縣",
    "513": "彰化縣", "514": "彰化縣", "515": "彰化縣", "516": "彰化縣",
    "520": "南投縣", "521": "南投縣", "522": "南投縣", "523": "南投縣",
    "545": "南投縣", "546": "南投縣",
    "600": "嘉義市", "602": "嘉義縣", "603": "嘉義縣", "604": "嘉義縣",
    "605": "嘉義縣",
    "630": "雲林縣", "631": "雲林縣", "632": "雲林縣", "633": "雲林縣",
    "640": "雲林縣", "641": "雲林縣",
    "700": "台南市", "701": "台南市", "702": "台南市", "703": "台南市",
    "704": "台南市", "708": "台南市", "709": "台南市", "710": "台南市",
    "711": "台南市", "712": "台南市", "713": "台南市", "714": "台南市",
    "715": "台南市", "716": "台南市", "717": "台南市", "718": "台南市",
    "719": "台南市", "720": "台南市", "721": "台南市", "722": "台南市",
    "723": "台南市", "724": "台南市", "725": "台南市", "726": "台南市",
    "730": "台南市", "731": "台南市", "732": "台南市", "733": "台南市",
    "734": "台南市", "735": "台南市", "736": "台南市",
    "800": "高雄市", "801": "高雄市", "802": "高雄市", "803": "高雄市",
    "804": "高雄市", "805": "高雄市", "806": "高雄市", "807": "高雄市",
    "811": "高雄市", "812": "高雄市", "813": "高雄市", "814": "高雄市",
    "815": "高雄市", "820": "高雄市", "821": "高雄市", "822": "高雄市",
    "823": "高雄市", "824": "高雄市", "825": "高雄市", "826": "高雄市",
    "827": "高雄市", "828": "高雄市", "829": "高雄市", "830": "高雄市",
    "831": "高雄市", "832": "高雄市", "833": "高雄市", "840": "高雄市",
    "842": "高雄市", "843": "高雄市", "844": "高雄市", "845": "高雄市",
    "846": "高雄市", "847": "高雄市",
    "900": "屏東縣", "901": "屏東縣", "902": "屏東縣", "903": "屏東縣",
    "904": "屏東縣", "905": "屏東縣", "906": "屏東縣", "907": "屏東縣",
    "908": "屏東縣", "909": "屏東縣", "911": "屏東縣", "912": "屏東縣",
    "913": "屏東縣", "920": "屏東縣", "921": "屏東縣", "922": "屏東縣",
    "923": "屏東縣", "924": "屏東縣", "925": "屏東縣", "926": "屏東縣",
    "927": "屏東縣", "928": "屏東縣", "929": "屏東縣", "931": "屏東縣",
    "932": "屏東縣", "940": "屏東縣", "941": "屏東縣", "942": "屏東縣",
    "943": "屏東縣", "944": "屏東縣", "945": "屏東縣", "946": "屏東縣",
    "947": "屏東縣", "950": "屏東縣", "951": "屏東縣", "952": "屏東縣",
    "953": "屏東縣", "954": "屏東縣", "955": "屏東縣", "956": "屏東縣",
    "957": "屏東縣", "958": "屏東縣", "966": "屏東縣",
    "950": "台東縣", "951": "台東縣", "952": "台東縣", "953": "台東縣",
    "970": "花蓮縣", "971": "花蓮縣", "972": "花蓮縣", "973": "花蓮縣",
    "974": "花蓮縣", "975": "花蓮縣", "976": "花蓮縣", "977": "花蓮縣",
    "978": "花蓮縣", "981": "花蓮縣", "983": "花蓮縣",
}


def zip_to_county(zipcode: str) -> str:
    return ZIPCODE_TO_COUNTY.get(zipcode[:3], "其他")


def load_county_counts(year: int, data_dir: Path = DATA_DIR) -> dict[str, int]:
    path = data_dir / f"{year}年新生資料庫.csv"
    result: dict[str, int] = {}
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            zipcode = row["郵遞區號"].strip()
            county = zip_to_county(zipcode)
            result[county] = result.get(county, 0) + 1
    return result


def get_top_counties(all_years: dict[int, dict], top_n: int = 10) -> list[str]:
    totals: dict[str, int] = {}
    for year_data in all_years.values():
        for county, count in year_data.items():
            totals[county] = totals.get(county, 0) + count
    sorted_counties = sorted(totals.items(), key=lambda x: -x[1])
    return [county for county, _ in sorted_counties[:top_n]]


def plot_heatmap(year_data: dict[int, dict], top_counties: list[str]):
    _apply_cjk_font()

    data = np.zeros((len(top_counties), len(YEARS)))
    for i, county in enumerate(top_counties):
        for j, year in enumerate(YEARS):
            data[i, j] = year_data[year].get(county, 0)

    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(data, cmap="YlOrRd", aspect="auto")

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("人數", fontsize=12)

    ax.set_xticks(range(len(YEARS)))
    ax.set_xticklabels([f"{y} 學年" for y in YEARS], fontsize=11)
    ax.set_yticks(range(len(top_counties)))
    ax.set_yticklabels(top_counties, fontsize=11)
    ax.set_title("109–114 學年各縣市招生人數熱力圖", fontsize=16, fontweight="bold")

    for i in range(len(top_counties)):
        for j in range(len(YEARS)):
            val = int(data[i, j])
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, color="black" if val < data.max() * 0.6 else "white")

    fig.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "task2.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Task 2 圖表已儲存：{path}")
    plt.close(fig)


def main():
    year_data = {}
    for year in YEARS:
        year_data[year] = load_county_counts(year)

    top_counties = get_top_counties(year_data, top_n=10)
    print("Top counties:", top_counties)

    plot_heatmap(year_data, top_counties)


if __name__ == "__main__":
    main()
