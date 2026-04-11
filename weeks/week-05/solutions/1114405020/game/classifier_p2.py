"""
P2 - 牌型分類
實現 HandClassifier 類別的分類和比較邏輯
"""

from enum import Enum


class CardType(Enum):
    """牌型列舉"""

    SINGLE = 1  # 單張
    PAIR = 2  # 對子
    TRIPLE = 3  # 三條
    STRAIGHT = 4  # 順子
    FLUSH = 5  # 同花
    FULL_HOUSE = 6  # 葫芦
    FOUR_OF_A_KIND = 7  # 四條
    STRAIGHT_FLUSH = 8  # 同花順


class HandClassifier:
    """牌型分類和比較"""

    @staticmethod
    def _is_straight(ranks):
        """
        檢查是否為順子

        Args:
            ranks: 排序後的點數列表

        Returns:
            bool: 是否為順子
        """
        if len(ranks) != 5:
            return False

        # 檢查一般順子
        if ranks[4] - ranks[0] == 4 and len(set(ranks)) == 5:
            return True

        # 檢查特殊情況：A-2-3-4-5（輪牌）
        if ranks == [3, 4, 5, 14, 15]:
            return True

        return False

    @staticmethod
    def _is_flush(suits):
        """
        檢查是否為同花

        Args:
            suits: 花色列表

        Returns:
            bool: 是否為同花
        """
        return len(set(suits)) == 1

    @staticmethod
    def classify(cards):
        """
        分類牌型

        Args:
            cards: 牌列表

        Returns:
            tuple 或 None: (CardType, rank, suit) 或 None
        """
        if not cards:
            return None

        n = len(cards)
        ranks = sorted([card.rank for card in cards])
        suits = [card.suit for card in cards]

        # 單張
        if n == 1:
            return (CardType.SINGLE, cards[0].rank, cards[0].suit)

        # 對子
        if n == 2:
            if ranks[0] == ranks[1]:
                return (CardType.PAIR, ranks[0], 0)
            return None

        # 三條
        if n == 3:
            if ranks[0] == ranks[1] == ranks[2]:
                return (CardType.TRIPLE, ranks[0], 0)
            return None

        # 五張牌型
        if n == 5:
            rank_counts = {}
            for rank in ranks:
                rank_counts[rank] = rank_counts.get(rank, 0) + 1

            is_straight = HandClassifier._is_straight(ranks)
            is_flush = HandClassifier._is_flush(suits)

            # 同花順
            if is_straight and is_flush:
                # 找最大的牌作為代表
                if ranks == [3, 4, 5, 14, 15]:  # 輪牌
                    return (CardType.STRAIGHT_FLUSH, 5, 0)
                return (CardType.STRAIGHT_FLUSH, ranks[4], 0)

            # 四條
            counts = sorted(rank_counts.values())
            if counts == [1, 4]:
                for rank, count in rank_counts.items():
                    if count == 4:
                        return (CardType.FOUR_OF_A_KIND, rank, 0)

            # 葫芦（3+2）
            if counts == [2, 3]:
                for rank, count in rank_counts.items():
                    if count == 3:
                        return (CardType.FULL_HOUSE, rank, 0)

            # 同花
            if is_flush:
                return (CardType.FLUSH, max(ranks), 0)

            # 順子
            if is_straight:
                if ranks == [3, 4, 5, 14, 15]:  # 輪牌
                    return (CardType.STRAIGHT, 5, 0)
                return (CardType.STRAIGHT, ranks[4], 0)

        return None

    @staticmethod
    def compare(play1, play2):
        """
        比較兩手牌大小

        Args:
            play1: 第一手牌
            play2: 第二手牌

        Returns:
            int: 1=play1大, -1=play2大, 0=平手
        """
        if not play1 or not play2:
            return 0

        classify1 = HandClassifier.classify(play1)
        classify2 = HandClassifier.classify(play2)

        if not classify1 or not classify2:
            return 0

        type1, rank1, suit1 = classify1
        type2, rank2, suit2 = classify2

        # 不同牌型：牌型大者獲勝
        if type1.value != type2.value:
            return 1 if type1.value > type2.value else -1

        # 相同牌型：比點數
        if rank1 != rank2:
            return 1 if rank1 > rank2 else -1

        # 相同點數：比花色（只對單張和對子有意義）
        if suit1 != suit2:
            return 1 if suit1 > suit2 else -1

        return 0

    @staticmethod
    def can_play(last_play, cards):
        """
        檢查是否可以出牌

        Args:
            last_play: 上家出牌，為 None 表示第一輪
            cards: 要出的牌

        Returns:
            bool: 是否可以出牌
        """
        classify_result = HandClassifier.classify(cards)

        if not classify_result:
            return False

        # 第一輪只能出 3♣
        if last_play is None:
            if len(cards) == 1 and cards[0].rank == 3 and cards[0].suit == 0:
                return True
            return False

        last_classify = HandClassifier.classify(last_play)
        if not last_classify:
            return False

        # 牌數必須相同
        if len(cards) != len(last_play):
            return False

        # 牌型必須相同
        if classify_result[0] != last_classify[0]:
            return False

        # 必須比上家大
        return HandClassifier.compare(cards, last_play) > 0
