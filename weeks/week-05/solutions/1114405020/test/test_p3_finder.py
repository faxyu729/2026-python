"""
P3 - 牌型搜尋測試
測試 HandFinder 類別的搜尋功能
"""

import unittest
from itertools import combinations
from game.models_p1 import Card, Hand
from game.classifier_p2 import CardType


class HandFinder:
    """找出所有可能的牌型組合"""

    @staticmethod
    def find_singles(hand):
        """
        找出所有單張

        Args:
            hand: Hand 物件

        Returns:
            list: [[card1], [card2], ...]
        """
        return [[card] for card in hand]

    @staticmethod
    def find_pairs(hand):
        """
        找出所有對子

        Args:
            hand: Hand 物件

        Returns:
            list: [[card1, card2], ...]
        """
        pairs = []
        rank_cards = {}

        # 按點數分組
        for card in hand:
            if card.rank not in rank_cards:
                rank_cards[card.rank] = []
            rank_cards[card.rank].append(card)

        # 對每個點數有2張以上的情況，產生所有組合
        for rank, cards in rank_cards.items():
            if len(cards) >= 2:
                for pair in combinations(cards, 2):
                    pairs.append(list(pair))

        return pairs

    @staticmethod
    def find_triples(hand):
        """
        找出所有三條

        Args:
            hand: Hand 物件

        Returns:
            list: [[card1, card2, card3], ...]
        """
        triples = []
        rank_cards = {}

        # 按點數分組
        for card in hand:
            if card.rank not in rank_cards:
                rank_cards[card.rank] = []
            rank_cards[card.rank].append(card)

        # 對每個點數有3張以上的情況，產生所有組合
        for rank, cards in rank_cards.items():
            if len(cards) >= 3:
                for triple in combinations(cards, 3):
                    triples.append(list(triple))

        return triples

    @staticmethod
    def _find_straight_from(hand, start_rank):
        """
        從指定點數開始尋找順子

        Args:
            hand: Hand 物件
            start_rank: 起始點數

        Returns:
            list 或 None: 五張牌列表或 None
        """
        hand_ranks = [card.rank for card in hand]
        hand_dict = {card.rank: card for card in hand}

        # 檢查是否有 5 張連續牌
        found = []
        for i in range(5):
            if (start_rank + i) in hand_dict:
                found.append(hand_dict[start_rank + i])
            else:
                return None

        return found

    @staticmethod
    def find_fives(hand):
        """
        找出所有五張牌型

        Args:
            hand: Hand 物件

        Returns:
            list: [[card1, card2, card3, card4, card5], ...]
        """
        from game.classifier_p2 import HandClassifier

        fives = []

        # 列舉所有 5 張牌組合
        for five_cards in combinations(hand, 5):
            classify_result = HandClassifier.classify(list(five_cards))
            if classify_result and classify_result[0] in [
                CardType.STRAIGHT,
                CardType.FLUSH,
                CardType.FULL_HOUSE,
                CardType.FOUR_OF_A_KIND,
                CardType.STRAIGHT_FLUSH,
            ]:
                fives.append(list(five_cards))

        return fives

    @staticmethod
    def get_all_valid_plays(hand, last_play):
        """
        找出所有合法出牌

        Args:
            hand: Hand 物件
            last_play: 上家出牌（None 表示第一輪）

        Returns:
            list: 所有合法出牌列表
        """
        from game.classifier_p2 import HandClassifier

        valid_plays = []

        # 第一輪：只能出 3♣
        if last_play is None:
            three_clubs = hand.find_3_clubs()
            if three_clubs:
                return [[three_clubs]]
            return []

        # 根據上家牌型，找相同牌型的更大牌
        last_classify = HandClassifier.classify(last_play)
        if not last_classify:
            return []

        last_type = last_classify[0]
        last_len = len(last_play)

        # 根據牌型長度找相應組合
        if last_len == 1:
            candidates = HandFinder.find_singles(hand)
        elif last_len == 2:
            candidates = HandFinder.find_pairs(hand)
        elif last_len == 3:
            candidates = HandFinder.find_triples(hand)
        elif last_len == 5:
            candidates = HandFinder.find_fives(hand)
        else:
            return []

        # 篩選可以出的牌
        for candidate in candidates:
            if HandClassifier.can_play(last_play, candidate):
                valid_plays.append(candidate)

        return valid_plays


class TestFindSingles(unittest.TestCase):
    """單張搜尋測試"""

    def test_find_singles(self):
        """測試：找出所有單張"""
        hand = Hand([Card(14, 3), Card(13, 2), Card(3, 0)])
        singles = HandFinder.find_singles(hand)
        self.assertEqual(len(singles), 3)

    def test_find_singles_empty(self):
        """測試：空手牌"""
        hand = Hand([])
        singles = HandFinder.find_singles(hand)
        self.assertEqual(len(singles), 0)


class TestFindPairs(unittest.TestCase):
    """對子搜尋測試"""

    def test_find_pairs_one(self):
        """測試：找到一個對子"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(3, 0)])
        pairs = HandFinder.find_pairs(hand)
        self.assertEqual(len(pairs), 1)

    def test_find_pairs_two(self):
        """測試：找到兩個對子"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(13, 1), Card(13, 0)])
        pairs = HandFinder.find_pairs(hand)
        self.assertEqual(len(pairs), 2)

    def test_find_pairs_none(self):
        """測試：找不到對子"""
        hand = Hand([Card(14, 3), Card(13, 2), Card(3, 0)])
        pairs = HandFinder.find_pairs(hand)
        self.assertEqual(len(pairs), 0)


class TestFindTriples(unittest.TestCase):
    """三條搜尋測試"""

    def test_find_triples_one(self):
        """測試：找到一個三條"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(14, 1), Card(3, 0)])
        triples = HandFinder.find_triples(hand)
        self.assertEqual(len(triples), 1)

    def test_find_triples_with_extra(self):
        """測試：有額外牌不影響三條搜尋"""
        hand = Hand([Card(14, 3), Card(14, 2), Card(14, 1), Card(13, 1), Card(13, 0)])
        triples = HandFinder.find_triples(hand)
        self.assertEqual(len(triples), 1)


class TestFindFives(unittest.TestCase):
    """五張牌型搜尋測試"""

    def test_find_straight(self):
        """測試：找順子"""
        hand = Hand(
            [
                Card(3, 0),
                Card(4, 1),
                Card(5, 2),
                Card(6, 3),
                Card(7, 0),
                Card(8, 1),
                Card(9, 2),
            ]
        )
        fives = HandFinder.find_fives(hand)
        # 應該找到至少一個順子
        self.assertGreater(len(fives), 0)

    def test_find_flush(self):
        """測試：找同花"""
        hand = Hand(
            [Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0), Card(14, 1)]
        )
        fives = HandFinder.find_fives(hand)
        self.assertGreater(len(fives), 0)


class TestGetAllValidPlays(unittest.TestCase):
    """合法出牌搜尋測試"""

    def test_first_turn(self):
        """測試：第一輪只能出 3♣"""
        hand = Hand([Card(3, 0), Card(14, 3), Card(5, 1)])
        valid = HandFinder.get_all_valid_plays(hand, None)
        self.assertEqual(len(valid), 1)
        self.assertEqual(valid[0][0].rank, 3)
        self.assertEqual(valid[0][0].suit, 0)

    def test_with_last_single(self):
        """測試：上家出單張，回傳單張選項"""
        hand = Hand([Card(6, 0), Card(7, 1), Card(14, 3)])
        last_play = [Card(5, 0)]
        valid = HandFinder.get_all_valid_plays(hand, last_play)
        # 應該有單張選項
        for play in valid:
            self.assertEqual(len(play), 1)

    def test_with_last_pair(self):
        """測試：上家出對子，回傳對子選項"""
        hand = Hand([Card(6, 0), Card(6, 1), Card(14, 3), Card(14, 2)])
        last_play = [Card(5, 0), Card(5, 1)]
        valid = HandFinder.get_all_valid_plays(hand, last_play)
        # 應該有對子選項
        for play in valid:
            self.assertEqual(len(play), 2)

    def test_no_valid(self):
        """測試：無法大於上家時"""
        hand = Hand([Card(3, 0), Card(4, 1), Card(5, 2)])
        last_play = [Card(14, 3), Card(14, 2)]  # 對 A
        valid = HandFinder.get_all_valid_plays(hand, last_play)
        # 手中沒有更大的對子
        self.assertEqual(len(valid), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
