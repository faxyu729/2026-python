"""
P3 - 牌型搜尋
實現 HandFinder 類別的搜尋功能
"""

from itertools import combinations
from game.classifier_p2 import CardType, HandClassifier


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
