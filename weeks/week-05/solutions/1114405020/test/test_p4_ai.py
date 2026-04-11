"""
P4 - AI 策略測試
測試 AIStrategy 類別的評分和選擇邏輯
"""

import unittest
from game.models_p1 import Card, Hand
from game.classifier_p2 import CardType


class AIStrategy:
    """AI 策略和評分"""

    # 評分常數
    TYPE_SCORES = {
        CardType.SINGLE: 1,
        CardType.PAIR: 2,
        CardType.TRIPLE: 3,
        CardType.STRAIGHT: 4,
        CardType.FLUSH: 5,
        CardType.FULL_HOUSE: 6,
        CardType.FOUR_OF_A_KIND: 7,
        CardType.STRAIGHT_FLUSH: 8,
    }

    EMPTY_HAND_BONUS = 10000
    NEAR_EMPTY_BONUS = 500
    SPADE_BONUS = 5

    @staticmethod
    def score_play(cards, hand, is_first=False):
        """
        評分牌組

        Args:
            cards: 要出的牌
            hand: 玩家的手牌
            is_first: 是否為第一輪

        Returns:
            float: 評分
        """
        from game.classifier_p2 import HandClassifier

        classify_result = HandClassifier.classify(cards)
        if not classify_result:
            return -1

        card_type, rank, _ = classify_result

        # 基礎分數：牌型分×100 + 點數×10
        score = AIStrategy.TYPE_SCORES[card_type] * 100 + rank * 10

        # 計算出牌後剩餘手牌數
        remaining = len(hand) - len(cards)

        # 獎勵分
        if remaining == 0:
            score += AIStrategy.EMPTY_HAND_BONUS
        elif remaining <= 3:
            score += AIStrategy.NEAR_EMPTY_BONUS

        # 黑桃獎勵
        spade_count = sum(1 for card in cards if card.suit == 3)
        score += spade_count * AIStrategy.SPADE_BONUS

        return score

    @staticmethod
    def select_best(valid_plays, hand, is_first=False):
        """
        選擇最佳出牌

        Args:
            valid_plays: 合法出牌列表
            hand: 玩家的手牌
            is_first: 是否為第一輪

        Returns:
            list 或 None: 最佳出牌或 None
        """
        if not valid_plays:
            return None

        # 第一輪：只能選 3♣
        if is_first:
            return valid_plays[0] if valid_plays else None

        # 選分數最高的
        best_play = None
        best_score = -1

        for play in valid_plays:
            score = AIStrategy.score_play(play, hand, is_first)
            if score > best_score:
                best_score = score
                best_play = play

        return best_play


class TestScorePlay(unittest.TestCase):
    """評分函數測試"""

    def test_score_single(self):
        """測試：單張評分"""
        hand = Hand([Card(14, 3), Card(14, 2)])
        score = AIStrategy.score_play([Card(14, 3)], hand)
        # 牌型1×100 + 14×10 + 黑桃獎勵1×5 + 剩1張獎勵10000 = 100 + 140 + 5 + 500 = 745
        # 剩1張有 NEAR_EMPTY_BONUS (500)
        expected = 1 * 100 + 14 * 10 + 1 * 5 + 500
        self.assertEqual(score, expected)

    def test_score_pair_higher(self):
        """測試：對子分數 > 單張分數"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(5, 0)])
        score_pair = AIStrategy.score_play([Card(14, 3), Card(14, 2)], hand)
        score_single = AIStrategy.score_play([Card(5, 0)], hand)
        self.assertGreater(score_pair, score_single)

    def test_score_triple_higher(self):
        """測試：三條分數 > 對子分數"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(14, 1)])
        score_triple = AIStrategy.score_play(
            [Card(14, 3), Card(14, 2), Card(14, 1)], hand
        )
        score_pair = AIStrategy.score_play([Card(14, 3), Card(14, 2)], hand)
        self.assertGreater(score_triple, score_pair)

    def test_score_near_empty(self):
        """測試：剩1張時有獎勵"""
        hand = Hand([Card(14, 3)])
        score = AIStrategy.score_play([Card(14, 3)], hand)
        # 應該有 EMPTY_HAND_BONUS
        self.assertGreater(score, 1000)

    def test_score_low_cards(self):
        """測試：剩2張時有獎勵"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(5, 0)])
        score = AIStrategy.score_play([Card(5, 0)], hand)
        # 應該有 NEAR_EMPTY_BONUS
        self.assertGreater(score, 500)

    def test_score_spade_bonus(self):
        """測試：黑桃額外加分"""
        hand = Hand([Card(14, 3), Card(5, 0)])
        score_spade = AIStrategy.score_play([Card(14, 3)], hand)
        hand2 = Hand([Card(14, 0), Card(5, 0)])
        score_club = AIStrategy.score_play([Card(14, 0)], hand2)
        # 黑桃應該比梅花高
        self.assertGreater(score_spade, score_club)


class TestSelectBest(unittest.TestCase):
    """選擇最佳出牌測試"""

    def test_select_best(self):
        """測試：在多個選項中選最佳"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(5, 0), Card(6, 1)])
        valid_plays = [[Card(5, 0)], [Card(14, 3), Card(14, 2)]]
        best = AIStrategy.select_best(valid_plays, hand)
        # 應該選對子（分數更高）
        self.assertEqual(len(best), 2)

    def test_select_first_turn(self):
        """測試：第一輪選 3♣"""
        hand = Hand([Card(3, 0), Card(14, 3), Card(5, 0)])
        valid_plays = [[Card(3, 0)]]
        best = AIStrategy.select_best(valid_plays, hand, is_first=True)
        self.assertEqual(best[0].rank, 3)
        self.assertEqual(best[0].suit, 0)

    def test_select_empty(self):
        """測試：無合法出牌"""
        hand = Hand([Card(3, 0), Card(4, 0)])
        best = AIStrategy.select_best([], hand)
        self.assertIsNone(best)


class TestAIStrategy(unittest.TestCase):
    """完整策略測試"""

    def test_ai_always_plays(self):
        """測試：有牌出時一定出"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(5, 0)])
        valid_plays = [[Card(5, 0)], [Card(14, 3), Card(14, 2)]]
        best = AIStrategy.select_best(valid_plays, hand)
        self.assertIsNotNone(best)

    def test_ai_prefers_high(self):
        """測試：優先選較大的牌"""
        hand = Hand([Card(3, 0), Card(4, 0), Card(14, 3)])
        valid_plays = [[Card(3, 0)], [Card(14, 3)]]
        best = AIStrategy.select_best(valid_plays, hand)
        self.assertEqual(best[0].rank, 14)

    def test_ai_try_empty(self):
        """測試：剩最後一張時優先選"""
        hand = Hand([Card(14, 3)])
        valid_plays = [[Card(14, 3)]]
        best = AIStrategy.select_best(valid_plays, hand)
        self.assertIsNotNone(best)


if __name__ == "__main__":
    unittest.main(verbosity=2)
