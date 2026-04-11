"""
赤壁戰役 - AI 簡化版本
Week 02-07 統合版本，使用 Counter 和 defaultdict 進行統計
(這是比較簡潔的實現方式)
"""

from collections import namedtuple, Counter, defaultdict

# Week 02: namedtuple 結構體
General = namedtuple(
    "General", ["faction", "name", "hp", "atk", "def_", "spd", "is_leader"]
)


class ChibiBattleEasy:
    """赤壁戰役引擎 - 簡化版"""

    def __init__(self):
        self.generals = {}
        self.stats = {"damage": Counter(), "losses": defaultdict(int)}

    def load_generals(self, filename):
        """讀取武將資料 (Week 07 檔案 I/O)"""
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "EOF":
                    break
                if not line:
                    continue

                parts = line.split()
                general = General(
                    faction=parts[0],
                    name=parts[1],
                    hp=int(parts[2]),
                    atk=int(parts[3]),
                    def_=int(parts[4]),
                    spd=int(parts[5]),
                    is_leader=(parts[6] == "True"),
                )
                self.generals[general.name] = general

    def get_battle_order(self):
        """按速度排序 (Week 02: sorted)"""
        return sorted(self.generals.values(), key=lambda g: g.spd, reverse=True)

    def calculate_damage(self, attacker_name, defender_name):
        """計算並累加傷害"""
        a, d = self.generals[attacker_name], self.generals[defender_name]
        damage = max(1, a.atk - d.def_)
        self.stats["damage"][attacker_name] += damage
        self.stats["losses"][defender_name] += damage
        return damage

    def simulate_battle(self):
        """模擬三波戰役"""
        shu = [g for g in self.generals.values() if g.faction == "蜀"]
        wu = [g for g in self.generals.values() if g.faction == "吳"]
        wei = [g for g in self.generals.values() if g.faction == "魏"]

        # 三波戰鬥
        for wave in range(1, 4):
            for attacker in shu[:wave]:
                if wave - 1 < len(wei):
                    self.calculate_damage(attacker.name, wei[wave - 1].name)
            for attacker in wu[:wave]:
                if wave - 1 < len(wei):
                    self.calculate_damage(attacker.name, wei[wave - 1].name)

    def get_damage_ranking(self, top_n=5):
        """傷害排名"""
        return self.stats["damage"].most_common(top_n)

    def get_faction_stats(self):
        """勢力傷害統計"""
        faction_damage = defaultdict(int)
        for name, dmg in self.stats["damage"].items():
            faction_damage[self.generals[name].faction] += dmg
        return dict(faction_damage)

    def print_report(self):
        """列印報告"""
        print("╔═══════════════════════════════════════════════════════╗")
        print("║              【赤壁戰役 - 傷害統計報告】                ║")
        print("╚═══════════════════════════════════════════════════════╝\n")

        print("【傷害輸出排名】")
        for i, (name, dmg) in enumerate(self.get_damage_ranking(), 1):
            bar = "=" * (dmg // 5) + "-" * (20 - dmg // 5)
            print(f"  {i}. {name:8} [{bar}] {dmg:3} HP")

        print("\n【勢力傷害統計】")
        for faction, total in sorted(
            self.get_faction_stats().items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {faction} : {total} HP")

        print("\n" + "=" * 57)


if __name__ == "__main__":
    import os

    game = ChibiBattleEasy()
    # 獲取指令碼所在目錄的上一級目錄
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    generals_file = os.path.join(parent_dir, "generals.txt")
    game.load_generals(generals_file)
    game.simulate_battle()
    game.print_report()
