"""
赤壁戰役 - 三國戰役模擬系統 (Week 02-07 統合)
Week 02: sorted, Counter, defaultdict, namedtuple
Week 07: 檔案 I/O, EOF 輸入處理
"""

from collections import namedtuple, Counter, defaultdict

# Week 02: namedtuple 結構體
General = namedtuple(
    "General", ["faction", "name", "hp", "atk", "def_", "spd", "is_leader"]
)


class ChibiBattle:
    """吞食天地戰役引擎"""

    def __init__(self):
        self.generals = {}
        # Week 02: Counter 和 defaultdict
        self.stats = {
            "damage": Counter(),  # 傷害統計
            "losses": defaultdict(int),  # 兵力損失
        }

    # ==================== Stage 1: 檔案 I/O ====================

    def load_generals(self, filename):
        """Week 07: 讀取武將資料，EOF 結尾"""
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # EOF 結尾處理
                if line == "EOF":
                    break
                if not line:
                    continue

                # 解析一行資料
                parts = line.split()
                faction, name, hp, atk, def_, spd, is_leader = parts

                # 建立 namedtuple
                general = General(
                    faction=faction,
                    name=name,
                    hp=int(hp),
                    atk=int(atk),
                    def_=int(def_),
                    spd=int(spd),
                    is_leader=(is_leader == "True"),
                )

                self.generals[name] = general

    # ==================== Stage 2: 戰鬥邏輯 ====================

    # Week 02: sorted() - 按速度排序
    def get_battle_order(self):
        """根據速度決定戰鬥順序"""
        return sorted(self.generals.values(), key=lambda g: g.spd, reverse=True)

    def calculate_damage(self, attacker_name, defender_name):
        """計算傷害: 攻擊 - 防禦"""
        attacker = self.generals[attacker_name]
        defender = self.generals[defender_name]

        damage = max(1, attacker.atk - defender.def_)

        # Week 02: Counter 自動累加
        self.stats["damage"][attacker_name] += damage
        self.stats["losses"][defender_name] += damage

        return damage

    def simulate_wave(self, wave_num):
        """模擬一波戰鬥"""
        shu = [g for g in self.generals.values() if g.faction == "蜀"]
        wu = [g for g in self.generals.values() if g.faction == "吳"]
        wei = [g for g in self.generals.values() if g.faction == "魏"]

        # 蜀軍攻擊
        for i, attacker in enumerate(shu[:wave_num]):
            if i < len(wei):
                self.calculate_damage(attacker.name, wei[i].name)

        # 吳軍攻擊
        for i, attacker in enumerate(wu[:wave_num]):
            if i < len(wei):
                self.calculate_damage(attacker.name, wei[i].name)

    def simulate_battle(self):
        """模擬三波完整戰役"""
        for wave in range(1, 4):
            self.simulate_wave(wave)

    # ==================== Stage 2: 統計與排名 ====================

    # Week 02: Counter.most_common()
    def get_damage_ranking(self, top_n=5):
        """傷害排名 (Top N)"""
        return self.stats["damage"].most_common(top_n)

    # Week 02: defaultdict + groupby 概念
    def get_faction_stats(self):
        """按勢力統計傷害"""
        faction_damage = defaultdict(int)

        for general_name, damage in self.stats["damage"].items():
            faction = self.generals[general_name].faction
            faction_damage[faction] += damage

        return dict(faction_damage)

    def get_defeated_generals(self):
        """取得戰敗將領"""
        defeated = []
        for name, total_loss in self.stats["losses"].items():
            if total_loss >= self.generals[name].hp:
                defeated.append(name)
        return defeated

    # ==================== Stage 3: 視覺化報告 ====================

    def print_battle_start(self):
        """列印戰役開始"""
        print("╔═══════════════════════════════════════════════════════╗")
        print("║        吞食天地 - 赤壁戰役 │ 蜀吳聯軍 vs 曹操魏軍      ║")
        print("╚═══════════════════════════════════════════════════════╝\n")

        # 列印各武將狀態
        for faction in ["蜀", "吳", "魏"]:
            print(f"【{faction}軍】")
            generals = [g for g in self.generals.values() if g.faction == faction]
            for g in sorted(generals, key=lambda x: x.spd, reverse=True):
                bar = "=" * (g.hp // 10) + "-" * (10 - g.hp // 10)
                leader = " (Military Advisor)" if g.is_leader else ""
                print(
                    f"  [*] {g.name:8} [{bar}] ATK{g.atk:2} DEF{g.def_:2} SPD{g.spd:2}{leader}"
                )
            print()

    def print_damage_report(self):
        """列印傷害統計報告"""
        print("╔═══════════════════════════════════════════════════════╗")
        print("║              【赤壁戰役 - 傷害統計報告】                ║")
        print("╚═══════════════════════════════════════════════════════╝\n")

        # Week 02: Counter.most_common()
        print("【傷害輸出排名 Top 5】")
        for i, (name, dmg) in enumerate(self.get_damage_ranking(), 1):
            bar = "=" * (dmg // 5) + "-" * (20 - dmg // 5)
            print(f"  {i}. {name:8} [{bar}] {dmg:3} HP")

        print("\n【兵力損失統計】")
        for name in sorted(
            self.stats["losses"].keys(),
            key=lambda x: self.stats["losses"][x],
            reverse=True,
        )[:5]:
            loss = self.stats["losses"][name]
            defeated = "[X]" if loss >= self.generals[name].hp else "[ ]"
            print(f"  {defeated} {name:8} : Lost {loss:3} HP")

        # Week 02: groupby 概念
        print("\n【勢力傷害統計】")
        faction_stats = self.get_faction_stats()
        max_damage = max(faction_stats.values()) if faction_stats else 1
        for faction in ["蜀", "吳", "魏"]:
            total = faction_stats.get(faction, 0)
            ratio = int(total / max_damage * 20) if max_damage else 0
            bar = "=" * ratio + "-" * (20 - ratio)
            percentage = (
                (total / sum(faction_stats.values()) * 100) if faction_stats else 0
            )
            print(f"  {faction} {bar} {total:3} HP ({percentage:5.1f}%)")

        print("\n" + "═" * 57)

    def run_full_battle(self):
        """執行完整戰役"""
        self.print_battle_start()
        print("【開始三波戰鬥...】\n")

        self.simulate_battle()

        print("\n【戰役完成】\n")
        self.print_damage_report()


if __name__ == "__main__":
    # 執行完整戰役
    import os

    game = ChibiBattle()
    # 獲取指令碼所在目錄的上一級目錄
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    generals_file = os.path.join(parent_dir, "generals.txt")
    game.load_generals(generals_file)
    game.run_full_battle()
