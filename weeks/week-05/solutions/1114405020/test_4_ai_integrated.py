"""
Phase 4: AI 策略 - 單元測試（整合版本）

本測試檔案驗證 AIStrategy 類別與 Phase 1-3 整合後的所有功能，包括：
1. 評分函數 - 計算出牌的得分
2. 選擇最佳出牌 - 從合法出牌中選擇最優選項
3. 完整策略 - 整合評分和選擇邏輯

測試涵蓋正常情況、邊界情況和特殊情況。
"""

import unittest
from game.models import Card, Hand, Deck
from game.classifier import CardType, HandClassifier
from game.ai import AIStrategy


class TestAIStrategyScoring(unittest.TestCase):
    """
    測試 AIStrategy 的評分函數

    驗證 score_play() 方法正確計算出牌的得分
    """

    def test_score_single_card(self):
        """
        測試單張牌評分

        出牌: ♠A (點數 14)
        手牌: 3 張 (♠A, ♣2, ♣3)
        出牌後剩 2 張，會有 NEAR_EMPTY_BONUS

        預期分數:
        - 牌型分: 1 × 100 = 100
        - 數字分: 14 × 10 = 140
        - 剩餘加分: 500 (剩 2 張)
        - 花色分: 1 × 5 = 5 (黑桃)
        - 總分: 100 + 140 + 500 + 5 = 745
        """
        hand = Hand([Card(14, 3), Card(15, 0), Card(3, 0)])  # ♠A, ♣2, ♣3
        cards = [Card(14, 3)]  # ♠A

        score = AIStrategy.score_play(cards, hand)

        # 預期分數 = 1×100 + 14×10 + 500 + 5 = 745
        self.assertEqual(score, 745.0)

    def test_score_pair_higher_than_single(self):
        """
        測試對子得分 > 單張得分

        出牌 1: ♠A (單張，點數 14)
        出牌 2: ♣4 + ♦4 (對子，點數 8)

        預期: 對子分數 > 單張分數
        因為牌型分數 (2×100 > 1×100) 足以補償點數差異
        """
        hand = Hand([Card(14, 3), Card(4, 0), Card(4, 1)] + [Card(3, 0)] * 10)

        single_score = AIStrategy.score_play([Card(14, 3)], hand)
        pair_score = AIStrategy.score_play([Card(4, 0), Card(4, 1)], hand)

        self.assertGreater(pair_score, single_score)

    def test_score_triple_higher_than_pair(self):
        """
        測試三條得分 > 對子得分

        出牌 1: ♣4 + ♦4 (對子)
        出牌 2: ♣4 + ♦4 + ♥4 (三條)

        預期: 三條分數 > 對子分數
        牌型分數 (3×100 > 2×100) 保證三條更強
        """
        hand = Hand([Card(4, 0), Card(4, 1), Card(4, 2)] + [Card(3, 0)] * 10)

        pair_score = AIStrategy.score_play([Card(4, 0), Card(4, 1)], hand)
        triple_score = AIStrategy.score_play([Card(4, 0), Card(4, 1), Card(4, 2)], hand)

        self.assertGreater(triple_score, pair_score)

    def test_score_near_empty_hand(self):
        """
        測試剩餘牌少時的加分

        情景: 玩家出牌後剩 1 張牌

        預期分數: > 10000
        包括基本分 + EMPTY_HAND_BONUS (10000)
        """
        hand = Hand([Card(5, 0), Card(5, 1)])  # 2 張牌
        cards = [Card(5, 0)]  # 出 1 張

        score = AIStrategy.score_play(cards, hand)

        # 應該包含 EMPTY_HAND_BONUS (10000)
        self.assertGreater(score, 10000)

    def test_score_low_cards_three_left(self):
        """
        測試剩 ≤ 3 張牌時的加分

        情景: 玩家出牌後剩 3 張牌

        預期分數: > 500 且 < 10000
        包括基本分 + NEAR_EMPTY_BONUS (500)
        """
        hand = Hand([Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0)])
        cards = [Card(6, 0)]

        score = AIStrategy.score_play(cards, hand)

        # 應該包含 NEAR_EMPTY_BONUS (500) 但不包含 EMPTY_HAND_BONUS
        self.assertGreater(score, 500)
        self.assertLess(score, 10000)

    def test_score_spade_bonus(self):
        """
        測試黑桃牌的加分

        比較:
        - 出牌 1: ♣3 (梅花 3，無加分)
        - 出牌 2: ♠3 (黑桃 3，有 +5 加分)

        預期: 黑桃分數 = 梅花分數 + 5
        """
        hand = Hand([Card(4, 0)] * 10 + [Card(3, 0), Card(3, 3)])

        club_score = AIStrategy.score_play([Card(3, 0)], hand)
        spade_score = AIStrategy.score_play([Card(3, 3)], hand)

        # 黑桃應該比梅花多 5 分
        self.assertEqual(spade_score - club_score, AIStrategy.SPADE_BONUS)

    def test_score_empty_cards_list(self):
        """
        測試空牌列表的評分

        出牌: [] (無牌)

        預期分數: 0
        """
        hand = Hand([Card(15, 0)])
        cards = []

        score = AIStrategy.score_play(cards, hand)

        self.assertEqual(score, 0.0)


class TestAIStrategySelection(unittest.TestCase):
    """
    測試 AIStrategy 的選擇函數

    驗證 select_best() 方法從合法出牌中選擇最優方案
    """

    def test_select_best_simple(self):
        """
        測試選擇最佳出牌 - 簡單情況

        合法出牌:
        1. ♣3 (單張，低分)
        2. ♣4 + ♦4 (對子，高分)
        3. ♠A (單張，中分)

        預期: 選擇對子 (♣4 + ♦4)
        """
        hand = Hand([Card(5, 0), Card(6, 0), Card(4, 0), Card(4, 1), Card(3, 0)])
        valid_plays = [[Card(3, 0)], [Card(4, 0), Card(4, 1)], [Card(14, 3)]]

        best = AIStrategy.select_best(valid_plays, hand)

        # 應該選擇對子
        self.assertEqual(len(best), 2)
        self.assertEqual(best[0].rank, 4)
        self.assertEqual(best[1].rank, 4)

    def test_select_first_turn_club_three(self):
        """
        測試第一回合選擇 - 必須出梅花 3

        情景: 遊戲開始，is_first=True

        合法出牌:
        1. ♣3 (梅花 3，必選)
        2. ♣5 (梅花 5)
        3. ♠A (黑桃 A)

        預期: 一定選擇 ♣3，不管其他牌多好
        """
        hand = Hand([Card(3, 0), Card(5, 0), Card(14, 3)])
        valid_plays = [[Card(3, 0)], [Card(5, 0)], [Card(14, 3)]]

        best = AIStrategy.select_best(valid_plays, hand, is_first=True)

        # 必須選擇梅花 3
        self.assertEqual(len(best), 1)
        self.assertEqual(best[0].rank, 3)
        self.assertEqual(best[0].suit, 0)

    def test_select_empty_valid_plays(self):
        """
        測試無合法出牌 - 返回 None

        情景: 沒有合法出牌，玩家必須過牌

        合法出牌: [] (空列表)

        預期: 返回 None
        """
        hand = Hand([Card(15, 0), Card(3, 0)])
        valid_plays = []

        best = AIStrategy.select_best(valid_plays, hand)

        self.assertIsNone(best)

    def test_select_prefers_higher_cards(self):
        """
        測試優先選擇高牌

        合法出牌:
        1. ♣3 (點數 3)
        2. ♣K (點數 13)
        3. ♣5 (點數 5)

        預期: 選擇 ♣K (最高牌)
        """
        hand = Hand([Card(3, 0), Card(13, 0), Card(5, 0)] + [Card(4, 0)] * 10)
        valid_plays = [[Card(3, 0)], [Card(13, 0)], [Card(5, 0)]]

        best = AIStrategy.select_best(valid_plays, hand)

        # 應該選擇 K (點數最高)
        self.assertEqual(best[0].rank, 13)

    def test_select_prefers_pair_over_single(self):
        """
        測試優先選擇對子而不是單張

        合法出牌:
        1. ♠2 (單張，點數最高)
        2. ♣3 + ♦3 (對子)

        預期: 選擇對子，因為牌型分高
        """
        hand = Hand([Card(15, 3), Card(3, 0), Card(3, 1)] + [Card(4, 0)] * 10)
        valid_plays = [[Card(15, 3)], [Card(3, 0), Card(3, 1)]]

        best = AIStrategy.select_best(valid_plays, hand)

        # 應該選擇對子
        self.assertEqual(len(best), 2)
        self.assertEqual(best[0].rank, 3)
        self.assertEqual(best[1].rank, 3)


class TestAIStrategyComplete(unittest.TestCase):
    """
    測試 AIStrategy 的完整策略

    驗證 AI 在不同遊戲情況下的表現
    """

    def test_ai_always_plays_when_legal(self):
        """
        測試 AI 有合法出牌時一定會出

        情景: 有多個合法出牌選擇

        預期: 返回值不為 None
        """
        hand = Hand([Card(3, 0), Card(5, 0), Card(14, 3)])
        valid_plays = [[Card(3, 0)], [Card(5, 0)], [Card(14, 3)]]

        best = AIStrategy.get_best_play(valid_plays, hand)

        # AI 一定會出牌
        self.assertIsNotNone(best)
        self.assertGreater(len(best), 0)

    def test_ai_prefers_high_over_low(self):
        """
        測試 AI 傾向選擇高牌而不是低牌

        情景: 有兩個單張選擇

        合法出牌:
        1. ♣3 (低牌)
        2. ♠A (高牌)

        預期: 選擇 ♠A (分數最高)
        """
        hand = Hand([Card(3, 0), Card(14, 3)] + [Card(4, 0)] * 20)
        valid_plays = [[Card(3, 0)], [Card(14, 3)]]

        best = AIStrategy.get_best_play(valid_plays, hand)

        # 應該選擇 A
        self.assertEqual(best[0].rank, 14)

    def test_ai_considers_hand_type(self):
        """
        測試 AI 考慮牌型的強度

        情景: 玩家有對子和單張可選

        合法出牌:
        1. ♠2 (單張，最高牌)
        2. ♣3 + ♦3 (對子，低牌)

        預期: 選擇對子，因為牌型優勢勝過點數劣勢
        """
        hand = Hand([Card(15, 3), Card(3, 0), Card(3, 1)] + [Card(5, 0)] * 20)
        valid_plays = [[Card(15, 3)], [Card(3, 0), Card(3, 1)]]

        best = AIStrategy.get_best_play(valid_plays, hand)

        # 應該選擇對子
        self.assertEqual(len(best), 2)


class TestAIStrategyEdgeCases(unittest.TestCase):
    """
    測試 AIStrategy 的邊界和特殊情況
    """

    def test_score_with_various_hand_sizes(self):
        """
        測試不同手牌數量的評分加分

        測試:
        - 剩 1 張: EMPTY_HAND_BONUS
        - 剩 2 張: NEAR_EMPTY_BONUS
        - 剩 3 張: NEAR_EMPTY_BONUS
        - 剩 4 張: 無加分
        - 剩 5 張+: 無加分
        """
        cards = [Card(5, 0)]

        # 剩 1 張
        hand1 = Hand([Card(6, 0)])
        score1 = AIStrategy.score_play(cards, hand1)
        self.assertGreater(score1, 10000)

        # 剩 2 張
        hand2 = Hand([Card(6, 0), Card(7, 0)])
        score2 = AIStrategy.score_play(cards, hand2)
        self.assertGreater(score2, 500)
        self.assertLess(score2, 10000)

        # 剩 3 張
        hand3 = Hand([Card(6, 0), Card(7, 0), Card(8, 0)])
        score3 = AIStrategy.score_play(cards, hand3)
        self.assertGreater(score3, 500)
        self.assertLess(score3, 10000)

        # 剩 4 張 (無加分)
        hand4 = Hand([Card(6, 0), Card(7, 0), Card(8, 0), Card(9, 0)])
        score4 = AIStrategy.score_play(cards, hand4)
        # score4 應該沒有加分，只有基本分
        self.assertLess(score4, 600)

    def test_select_consistency(self):
        """
        測試選擇結果的一致性

        同樣的輸入應該產生同樣的結果
        """
        hand = Hand([Card(5, 0), Card(6, 0)])
        valid_plays = [[Card(3, 0)], [Card(4, 0), Card(4, 1)]]

        best1 = AIStrategy.select_best(valid_plays, hand)
        best2 = AIStrategy.select_best(valid_plays, hand)

        # 結果應該相同
        self.assertEqual(len(best1), len(best2))
        self.assertEqual(best1[0].rank, best2[0].rank)
        self.assertEqual(best1[0].suit, best2[0].suit)


if __name__ == "__main__":
    # 設定詳細的測試輸出格式
    unittest.main(verbosity=2)
