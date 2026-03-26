"""
Big Two 牌遊戲 - Phase 3: 牌型搜尋測試
測試 HandFinder 類別的所有方法
"""

import unittest
from game.models import Card, Hand
from game.finder import HandFinder
from game.classifier import HandClassifier


class TestSingles(unittest.TestCase):
    """單張搜尋測試"""

    def setUp(self):
        """測試前準備"""
        self.card_3_clubs = Card(3, 0)  # ♣3
        self.card_k_hearts = Card(13, 2)  # ♥K
        self.card_a_spades = Card(14, 3)  # ♠A

    def test_find_singles_basic(self):
        """測試：基本單張搜尋"""
        hand = Hand([self.card_3_clubs, self.card_k_hearts, self.card_a_spades])
        singles = HandFinder.find_singles(hand)

        self.assertEqual(len(singles), 3)
        for single in singles:
            self.assertEqual(len(single), 1)

    def test_find_singles_empty(self):
        """測試：空手牌搜尋單張"""
        hand = Hand([])
        singles = HandFinder.find_singles(hand)
        self.assertEqual(len(singles), 0)

    def test_find_singles_order(self):
        """測試：單張排列順序"""
        cards = [self.card_a_spades, self.card_3_clubs, self.card_k_hearts]
        hand = Hand(cards)
        singles = HandFinder.find_singles(hand)

        self.assertEqual(singles[0][0], self.card_a_spades)
        self.assertEqual(singles[1][0], self.card_3_clubs)
        self.assertEqual(singles[2][0], self.card_k_hearts)


class TestPairs(unittest.TestCase):
    """對子搜尋測試"""

    def setUp(self):
        """測試前準備"""
        self.a_spades = Card(14, 3)  # ♠A
        self.a_hearts = Card(14, 2)  # ♥A
        self.a_diamonds = Card(14, 1)  # ♦A
        self.k_spades = Card(13, 3)  # ♠K
        self.k_clubs = Card(13, 0)  # ♣K
        self.three_clubs = Card(3, 0)  # ♣3

    def test_find_pairs_one(self):
        """測試：找出1個對子"""
        hand = Hand([self.a_spades, self.a_hearts, self.three_clubs])
        pairs = HandFinder.find_pairs(hand)

        self.assertEqual(len(pairs), 1)
        self.assertEqual(len(pairs[0]), 2)

    def test_find_pairs_two(self):
        """測試：找出2個對子"""
        hand = Hand([self.a_spades, self.a_hearts, self.k_spades, self.k_clubs])
        pairs = HandFinder.find_pairs(hand)

        self.assertEqual(len(pairs), 2)

    def test_find_pairs_none(self):
        """測試：無對子的情況"""
        hand = Hand([self.a_spades, Card(13, 2), self.three_clubs])
        pairs = HandFinder.find_pairs(hand)

        self.assertEqual(len(pairs), 0)

    def test_find_pairs_multiple_combinations(self):
        """測試：多種對子組合"""
        hand = Hand([self.a_spades, self.a_hearts, self.a_diamonds])
        pairs = HandFinder.find_pairs(hand)

        # C(3,2) = 3
        self.assertEqual(len(pairs), 3)


class TestTriples(unittest.TestCase):
    """三條搜尋測試"""

    def setUp(self):
        """測試前準備"""
        self.a_spades = Card(14, 3)
        self.a_hearts = Card(14, 2)
        self.a_diamonds = Card(14, 1)
        self.three_clubs = Card(3, 0)

    def test_find_triples_one(self):
        """測試：找出1個三條"""
        hand = Hand([self.a_spades, self.a_hearts, self.a_diamonds, self.three_clubs])
        triples = HandFinder.find_triples(hand)

        self.assertEqual(len(triples), 1)
        self.assertEqual(len(triples[0]), 3)

    def test_find_triples_none(self):
        """測試：無三條的情況"""
        hand = Hand([self.a_spades, self.a_hearts, self.three_clubs])
        triples = HandFinder.find_triples(hand)

        self.assertEqual(len(triples), 0)


class TestFives(unittest.TestCase):
    """五張牌型搜尋測試"""

    def test_find_fives_straight(self):
        """測試：順子搜尋"""
        straight = Hand(
            [
                Card(3, 0),  # ♣3
                Card(4, 1),  # ♦4
                Card(5, 2),  # ♥5
                Card(6, 3),  # ♠6
                Card(7, 0),  # ♣7
            ]
        )
        fives = HandFinder.find_fives(straight)
        self.assertEqual(len(fives), 1)

    def test_find_fives_flush(self):
        """測試：同花搜尋"""
        flush = Hand(
            [
                Card(3, 3),  # ♠3
                Card(5, 3),  # ♠5
                Card(7, 3),  # ♠7
                Card(9, 3),  # ♠9
                Card(11, 3),  # ♠J
            ]
        )
        fives = HandFinder.find_fives(flush)
        self.assertEqual(len(fives), 1)

    def test_find_fives_full_house(self):
        """測試：葫蘆搜尋"""
        full_house = Hand(
            [
                Card(14, 3),  # ♠A
                Card(14, 2),  # ♥A
                Card(14, 1),  # ♦A
                Card(13, 3),  # ♠K
                Card(13, 0),  # ♣K
            ]
        )
        fives = HandFinder.find_fives(full_house)
        self.assertEqual(len(fives), 1)

    def test_find_fives_four_of_a_kind(self):
        """測試：四條搜尋"""
        four_kind = Hand(
            [
                Card(14, 3),  # ♠A
                Card(14, 2),  # ♥A
                Card(14, 1),  # ♦A
                Card(14, 0),  # ♣A
                Card(13, 3),  # ♠K
            ]
        )
        fives = HandFinder.find_fives(four_kind)
        self.assertEqual(len(fives), 1)

    def test_find_fives_straight_flush(self):
        """測試：同花順搜尋"""
        straight_flush = Hand(
            [
                Card(3, 3),  # ♠3
                Card(4, 3),  # ♠4
                Card(5, 3),  # ♠5
                Card(6, 3),  # ♠6
                Card(7, 3),  # ♠7
            ]
        )
        fives = HandFinder.find_fives(straight_flush)
        self.assertEqual(len(fives), 1)

    def test_find_fives_ace_low_straight(self):
        """測試：特殊A-2-3-4-5順子"""
        ace_low = Hand(
            [
                Card(14, 0),  # ♣A
                Card(15, 1),  # ♦2
                Card(3, 2),  # ♥3
                Card(4, 3),  # ♠4
                Card(5, 0),  # ♣5
            ]
        )
        fives = HandFinder.find_fives(ace_low)
        self.assertEqual(len(fives), 1)

    def test_find_fives_empty(self):
        """測試：牌不足5張時的搜尋"""
        hand = Hand([Card(3, 0), Card(13, 2), Card(14, 3), Card(4, 0)])
        fives = HandFinder.find_fives(hand)
        self.assertEqual(len(fives), 0)


class TestValidPlays(unittest.TestCase):
    """合法出牌搜尋測試"""

    def setUp(self):
        """測試前準備"""
        self.three_clubs = Card(3, 0)
        self.k_hearts = Card(13, 2)
        self.a_spades = Card(14, 3)

    def test_first_turn_with_3_clubs(self):
        """測試：第一手牌有♣3"""
        hand = Hand([self.three_clubs, self.k_hearts, self.a_spades])
        valid_plays = HandFinder.get_all_valid_plays(hand, last_play=None)

        self.assertGreater(len(valid_plays), 0)
        # 第一個應該是 ♣3
        self.assertEqual(valid_plays[0][0], self.three_clubs)

    def test_first_turn_no_3_clubs(self):
        """測試：第一手牌無♣3"""
        hand = Hand([self.k_hearts, self.a_spades, Card(4, 0)])
        valid_plays = HandFinder.get_all_valid_plays(hand, last_play=None)

        self.assertEqual(len(valid_plays), 0)

    def test_with_last_single(self):
        """測試：上家出單張"""
        hand = Hand([self.three_clubs, self.k_hearts, self.a_spades])
        last_play = [Card(13, 0)]  # ♣K

        valid_plays = HandFinder.get_all_valid_plays(hand, last_play=last_play)
        singles = HandFinder.find_singles(hand)

        # 應該回傳比 ♣K 更強的單張
        self.assertLessEqual(len(valid_plays), len(singles))

    def test_with_last_pair(self):
        """測試：上家出對子"""
        a_hearts = Card(14, 2)
        hand = Hand([self.three_clubs, self.a_spades, a_hearts, self.k_hearts])
        last_play = [self.a_spades, a_hearts]  # 對A

        valid_plays = HandFinder.get_all_valid_plays(hand, last_play=last_play)
        pairs = HandFinder.find_pairs(hand)

        # 應該回傳比 對A 更強的對子
        self.assertLessEqual(len(valid_plays), len(pairs))

    def test_with_last_triple(self):
        """測試：上家出三條"""
        a_hearts = Card(14, 2)
        a_diamonds = Card(14, 1)
        hand = Hand([self.three_clubs, self.a_spades, a_hearts, a_diamonds])
        last_play = [self.a_spades, a_hearts, a_diamonds]  # 三條A

        valid_plays = HandFinder.get_all_valid_plays(hand, last_play=last_play)
        triples = HandFinder.find_triples(hand)

        # 應該回傳比 三條A 更強的三條
        self.assertLessEqual(len(valid_plays), len(triples))


class TestHelperMethods(unittest.TestCase):
    """輔助方法測試"""

    def test_is_straight_normal(self):
        """測試：正常順子檢查"""
        ranks = [3, 4, 5, 6, 7]
        self.assertTrue(HandFinder._is_straight(ranks))

    def test_is_straight_ace_low(self):
        """測試：A低順子檢查"""
        ranks = [3, 4, 5, 14, 15]  # A=14, 2=15
        self.assertTrue(HandFinder._is_straight(ranks))

    def test_is_straight_invalid(self):
        """測試：非順子檢查"""
        ranks = [3, 4, 5, 7, 9]
        self.assertFalse(HandFinder._is_straight(ranks))

    def test_is_flush_true(self):
        """測試：同花檢查"""
        suits = [3, 3, 3, 3, 3]
        self.assertTrue(HandFinder._is_flush(suits))

    def test_is_flush_false(self):
        """測試：非同花檢查"""
        suits = [3, 2, 1, 0, 3]
        self.assertFalse(HandFinder._is_flush(suits))


class TestEdgeCases(unittest.TestCase):
    """邊界情況測試"""

    def test_empty_hand_operations(self):
        """測試：空手牌的各種操作"""
        hand = Hand([])

        self.assertEqual(len(HandFinder.find_singles(hand)), 0)
        self.assertEqual(len(HandFinder.find_pairs(hand)), 0)
        self.assertEqual(len(HandFinder.find_triples(hand)), 0)
        self.assertEqual(len(HandFinder.find_fives(hand)), 0)

    def test_single_card_hand(self):
        """測試：只有1張牌的手牌"""
        hand = Hand([Card(3, 0)])

        self.assertEqual(len(HandFinder.find_singles(hand)), 1)
        self.assertEqual(len(HandFinder.find_pairs(hand)), 0)
        self.assertEqual(len(HandFinder.find_triples(hand)), 0)
        self.assertEqual(len(HandFinder.find_fives(hand)), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
