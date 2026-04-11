"""
P4 - AI 策略
實現 AIStrategy 類別的評分和選擇邏輯
"""

from game.classifier_p2 import CardType, HandClassifier


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
