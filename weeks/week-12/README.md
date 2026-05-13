# Week 12（115/05/11－115/05/17）

> 📢 **合併補課**：Week 11 停課（115/06/12 生成式 AI 論壇），本週合併上課。
> 上課順序：先補 Week 11（類別與模組），再接 Week 12（數論與位元運算）。

---

## Week 11 補課：類別與模組（封裝、矩陣與優化）

- 課堂範例：[`../week-11/in-class/`](../week-11/in-class/)
- 解題：[10409](../week-11/QUESTION-10409.md) | [10415](../week-11/QUESTION-10415.md) | [10420](../week-11/QUESTION-10420.md) | [10642](../week-11/QUESTION-10642.md) | [10783](../week-11/QUESTION-10783.md)

| 範例 | 主題 |
|------|------|
| [R01](../week-11/in-class/R01-class-basic.py) | `__init__` / 方法 / `__repr__` / 類別變數 vs 實例變數 |
| [R02](../week-11/in-class/R02-property.py) | `@property` / getter / setter / 唯讀屬性 |
| [R03](../week-11/in-class/R03-inheritance.py) | 繼承 / `super()` / 方法覆寫 / `isinstance` |
| [R04](../week-11/in-class/R04-special-methods.py) | `__eq__` / `__lt__` / `__len__` / `__iter__` / `@total_ordering` |
| [R05](../week-11/in-class/R05-dataclass.py) | `@dataclass` / `field` / `frozen` / `__post_init__` |
| [U01](../week-11/in-class/U01-die-game.py) | 骰子模擬：用 class 封裝狀態（對應 UVA 10409）|

| # | 題名 | 難度 | 題目檔 |
|---|------|------|------|
| 10409 | UVA 10409 — Die Game | ⭐ | [QUESTION-10409.md](../week-11/QUESTION-10409.md) |
| 10415 | UVA 10415 — Eb Alto Saxophone Player | ⭐ | [QUESTION-10415.md](../week-11/QUESTION-10415.md) |
| 10420 | UVA 10420 — List of Conquests | ⭐ | [QUESTION-10420.md](../week-11/QUESTION-10420.md) |
| 10642 | UVA 10642 — Can You Solve It? | ⭐ | [QUESTION-10642.md](../week-11/QUESTION-10642.md) |
| 10783 | UVA 10783 | ⭐ | [QUESTION-10783.md](../week-11/QUESTION-10783.md) |

---

## Week 12 本週：數論與位元運算

- 課堂範例：[`in-class/`](./in-class/)（4 記憶層 R + 1 理解層 U）
- 解題：[10812](./QUESTION-10812.md) | [10908](./QUESTION-10908.md) | [10922](./QUESTION-10922.md) | [10929](./QUESTION-10929.md) | [10931](./QUESTION-10931.md)
- 作業：完成 5 題並提交到 `weeks/week-12/solutions/<student-id>/`

| 範例 | 主題 |
|------|------|
| [R01](./in-class/R01-gcd-divisibility.py) | `math.gcd` / `math.lcm` / 數字位數和 / 9-degree |
| [R02](./in-class/R02-big-number.py) | 大數字串處理 / 11 的倍數判斷（奇偶位交替）|
| [R03](./in-class/R03-binary-bits.py) | `bin()` / `format(n,'b')` / 位元運算子 / 計算 1 的個數 |
| [R04](./in-class/R04-matrix-search.py) | 2D 矩陣中心擴張 / 找最大全同字元正方形 |
| [U01](./in-class/U01-number-theory.py) | 整合：Beat the Spread! / 2 the 9s / Can You Solve It? |

| # | 題名 | 難度 | 核心概念 |
|---|------|------|---------|
| 10812 | UVA 10812 — Beat the Spread! | ⭐ | 線性方程：`(S+D)/2`，判斷整數解與非負 |
| 10908 | UVA 10908 — Largest Square | ⭐ | 2D 矩陣中心擴張，最大全同字元正方形 |
| 10922 | UVA 10922 — 2 the 9s | ⭐ | 遞迴數字和，9 的倍數與深度 |
| 10929 | UVA 10929 | ⭐ | 大數（1000 位），11 的倍數判斷 |
| 10931 | UVA 10931 — Parity | ⭐ | 整數轉二進位，計算 1 的個數 |
