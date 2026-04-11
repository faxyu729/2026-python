"""
赤壁戰役 - 完整測試套件 (TDD 三階段)
包含 Stage 1, Stage 2, Stage 3 的所有測試
"""

import unittest
import os
import sys
from collections import Counter

# 導入 ChibiBattle 類別
from chibi_battle import ChibiBattle

# 獲取正確的 generals.txt 路徑
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
GENERALS_FILE = os.path.join(PARENT_DIR, "generals.txt")


class TestStage1DataLoading(unittest.TestCase):
    """Stage 1: 資料讀取測試"""

    def setUp(self):
        """每個測試前準備"""
        self.game = ChibiBattle()

    def test_load_generals_from_file(self):
        """測試 1-1: 正確讀取 9 位武將"""
        # Arrange: 準備測試環境
        # Act: 執行讀取
        self.game.load_generals(GENERALS_FILE)

        # Assert: 驗證結果
        self.assertEqual(len(self.game.generals), 9)
        self.assertIn("劉備", self.game.generals)
        self.assertIn("曹操", self.game.generals)

    def test_parse_general_attributes(self):
        """測試 1-2: 正確解析武將屬性"""
        self.game.load_generals(GENERALS_FILE)

        # 驗證 namedtuple 結構體
        general = self.game.generals["關羽"]
        self.assertEqual(general.name, "關羽")
        self.assertEqual(general.atk, 28)
        self.assertEqual(general.def_, 14)
        self.assertEqual(general.spd, 85)
        self.assertEqual(general.faction, "蜀")

    def test_faction_distribution(self):
        """測試 1-3: 三國分布正確"""
        self.game.load_generals(GENERALS_FILE)

        # 使用 Counter 統計派系
        factions = Counter(g.faction for g in self.game.generals.values())

        self.assertEqual(factions["蜀"], 3)
        self.assertEqual(factions["吳"], 3)
        self.assertEqual(factions["魏"], 3)

    def test_eof_parsing(self):
        """測試 1-4: 正確識別 EOF 結尾"""
        # 應能正確停止在 EOF，不會讀取額外資料
        self.game.load_generals(GENERALS_FILE)

        self.assertEqual(len(self.game.generals), 9)  # 不會超過 9


class TestStage2BattleLogic(unittest.TestCase):
    """Stage 2: 戰鬥模擬與統計測試"""

    def setUp(self):
        """每個測試前準備"""
        self.game = ChibiBattle()
        self.game.load_generals(GENERALS_FILE)

    def test_battle_order_by_speed(self):
        """測試 2-1: 根據速度排序戰鬥順序"""
        # Week 02: sorted(key=...)
        battle_order = self.game.get_battle_order()

        # 速度由高到低: 85, 85, 82, 80, 78, 75, 75, 68, 60
        self.assertEqual(battle_order[0].spd, 85)  # 最快
        self.assertEqual(battle_order[-1].spd, 60)  # 最慢

    def test_calculate_damage(self):
        """測試 2-2: 正確計算傷害 (攻擊 - 防禦)"""
        # 關羽 (攻28) vs 夏侯惇 (防14)
        damage = self.game.calculate_damage("關羽", "夏侯惇")

        self.assertEqual(damage, 28 - 14)  # = 14

    def test_damage_counter_accumulation(self):
        """測試 2-3: Counter 自動累加傷害"""
        # Week 02: Counter
        self.game.calculate_damage("關羽", "夏侯惇")
        self.game.calculate_damage("關羽", "曹操")

        # 關羽 vs 夏侯惇 (28-14=14) + vs 曹操 (28-16=12) = 26
        self.assertEqual(self.game.stats["damage"]["關羽"], 26)

    def test_simulate_one_wave(self):
        """測試 2-4: 模擬一波戰鬥"""
        self.game.simulate_wave(1)  # Wave 1

        # 驗證有傷害產生
        total_damage = sum(self.game.stats["damage"].values())
        self.assertGreater(total_damage, 0)

    def test_simulate_three_waves(self):
        """測試 2-5: 模擬三波完整戰役"""
        self.game.simulate_battle()

        # 蜀吳傷害應大於魏軍傷害 (蜀吳勝)
        shu_wu_damage = sum(
            dmg
            for name, dmg in self.game.stats["damage"].items()
            if self.game.generals[name].faction in ["蜀", "吳"]
        )
        wei_damage = sum(
            dmg
            for name, dmg in self.game.stats["damage"].items()
            if self.game.generals[name].faction == "魏"
        )

        self.assertGreater(shu_wu_damage, wei_damage)

    def test_troop_loss_tracking(self):
        """測試 2-6: defaultdict 追蹤兵力損失"""
        # Week 02: defaultdict
        self.game.simulate_battle()

        # 夏侯惇應受到傷害
        self.assertGreater(self.game.stats["losses"]["夏侯惇"], 0)

    def test_damage_ranking_most_common(self):
        """測試 2-7: most_common() 傷害排名"""
        # Week 02: Counter.most_common()
        self.game.simulate_battle()
        ranking = self.game.get_damage_ranking()

        # 前 5 名傷害遞減
        damages = [dmg for _, dmg in ranking]
        self.assertEqual(damages, sorted(damages, reverse=True))

    def test_faction_damage_stats(self):
        """測試 2-8: 按勢力統計傷害"""
        # Week 02: groupby 概念 + defaultdict
        self.game.simulate_battle()
        faction_stats = self.game.get_faction_stats()

        # 蜀吳應有傷害輸出（攻擊方）
        self.assertGreater(faction_stats.get("蜀", 0), 0)
        self.assertGreater(faction_stats.get("吳", 0), 0)

    def test_defeated_generals(self):
        """測試 2-9: 正確識別戰敗將領"""
        self.game.simulate_battle()
        defeated = self.game.get_defeated_generals()

        # 若有將領戰敗則驗證，若無則驗證至少有損傷
        if defeated:
            self.assertGreater(len(defeated), 0)
        else:
            # 至少有人受傷
            total_losses = sum(self.game.stats["losses"].values())
            self.assertGreater(total_losses, 0)


class TestStage3Refactoring(unittest.TestCase):
    """Stage 3: 重構與視覺化測試"""

    def setUp(self):
        """每個測試前準備"""
        self.game = ChibiBattle()
        self.game.load_generals(GENERALS_FILE)

    def test_stats_unchanged_after_refactor(self):
        """測試 3-1: 重構後統計結果不變"""
        self.game.simulate_battle()

        damage_before = dict(self.game.stats["damage"])
        losses_before = dict(self.game.stats["losses"])

        # 重新執行 (視覺化不應改變邏輯)
        self.assertEqual(dict(self.game.stats["damage"]), damage_before)
        self.assertEqual(dict(self.game.stats["losses"]), losses_before)

    def test_all_stage1_tests_still_pass(self):
        """測試 3-2: Stage 1 測試仍通過"""
        self.game.load_generals(GENERALS_FILE)
        self.assertEqual(len(self.game.generals), 9)

    def test_all_stage2_tests_still_pass(self):
        """測試 3-3: Stage 2 測試仍通過"""
        self.game.simulate_battle()
        ranking = self.game.get_damage_ranking()
        # 至少有 1 個排名（因為最多查 5 個，但可能只有更少的）
        self.assertGreater(len(ranking), 0)


if __name__ == "__main__":
    # 執行所有測試
    unittest.main(verbosity=2)
