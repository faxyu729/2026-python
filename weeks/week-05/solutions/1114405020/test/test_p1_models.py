"""
P1 - 資料模型測試
測試 Card、Deck、Hand、Player 四個基礎類別的功能
"""

import unittest
from itertools import combinations


# 花色符號對應表
SUIT_SYMBOLS = {0: "♣", 1: "♦", 2: "♥", 3: "♠"}
# 牌點數符號對應表
RANK_SYMBOLS = {
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "T",
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
    15: "2",
}


class Card:
    """代表一張撲克牌"""

    def __init__(self, rank, suit):
        """
        初始化撲克牌

        Args:
            rank: 牌點數 (3-15, 其中 14=A, 15=2)
            suit: 花色 (0=♣, 1=♦, 2=♥, 3=♠)
        """
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        """回傳牌的字符表示，例如 '♠A'"""
        suit_symbol = SUIT_SYMBOLS.get(self.suit, "?")
        rank_symbol = RANK_SYMBOLS.get(self.rank, "?")
        return f"{suit_symbol}{rank_symbol}"

    def __eq__(self, other):
        """比較兩張牌是否相同"""
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        """比較大小：先比點數，再比花色"""
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.suit < other.suit

    def __gt__(self, other):
        """比較大小：先比點數，再比花色"""
        if self.rank != other.rank:
            return self.rank > other.rank
        return self.suit > other.suit

    def __hash__(self):
        """用於集合和字典"""
        return hash((self.rank, self.suit))

    def to_sort_key(self):
        """回傳排序鍵值，形式為 (rank, suit) 元組"""
        return (self.rank, self.suit)


class Deck:
    """代表52張撲克牌堆"""

    def __init__(self):
        """初始化牌堆，建立52張完整牌組"""
        self.cards = self._create_cards()

    def _create_cards(self):
        """建立標準52張撲克牌組"""
        cards = []
        # 點數範圍：3-14（A），15（2）
        for rank in range(3, 16):
            # 花色：0=♣, 1=♦, 2=♥, 3=♠
            for suit in range(4):
                cards.append(Card(rank, suit))
        return cards

    def shuffle(self):
        """洗牌"""
        import random

        random.shuffle(self.cards)

    def deal(self, n):
        """
        發n張牌

        Args:
            n: 要發的牌數

        Returns:
            發出的牌列表，若牌數不足則發所有剩餘牌
        """
        cards_to_deal = min(n, len(self.cards))
        dealt = self.cards[:cards_to_deal]
        self.cards = self.cards[cards_to_deal:]
        return dealt


class Hand(list):
    """代表玩家的手牌，繼承 list"""

    def __init__(self, cards=None):
        """
        初始化手牌

        Args:
            cards: 牌的列表，如果為 None 則為空手牌
        """
        super().__init__()
        if cards:
            self.extend(cards)

    def sort_desc(self):
        """
        按點數降序、花色升序排序手牌
        排序順序：點數高到低，同點數則花色小到大
        """
        self.sort(key=lambda card: (-card.rank, card.suit))

    def find_3_clubs(self):
        """
        尋找3♣牌

        Returns:
            Card: 3♣牌，若無則回傳 None
        """
        for card in self:
            if card.rank == 3 and card.suit == 0:  # 3 和 ♣
                return card
        return None

    def remove(self, cards):
        """
        從手牌中移除指定的牌

        Args:
            cards: 要移除的牌列表
        """
        for card in cards:
            if card in self:
                super().remove(card)


class Player:
    """代表遊戲中的一位玩家"""

    def __init__(self, name, is_ai=False):
        """
        初始化玩家

        Args:
            name: 玩家名稱
            is_ai: 是否為 AI 玩家
        """
        self.name = name
        self.is_ai = is_ai
        self.hand = Hand()
        self.score = 0

    def take_cards(self, cards):
        """
        將牌加入手牌

        Args:
            cards: 要加入的牌列表
        """
        self.hand.extend(cards)

    def play_cards(self, cards):
        """
        出牌

        Args:
            cards: 要出的牌列表

        Returns:
            出的牌列表
        """
        self.hand.remove(cards)
        return cards


class TestCard(unittest.TestCase):
    """Card 類別的單元測試"""

    def test_card_creation(self):
        """測試：建立 Card 物件"""
        card = Card(rank=14, suit=3)
        self.assertEqual(card.rank, 14)
        self.assertEqual(card.suit, 3)

    def test_card_repr_ace(self):
        """測試：A 的字符表示應為 '♠A'"""
        card = Card(14, 3)
        self.assertEqual(repr(card), "♠A")

    def test_card_repr_three(self):
        """測試：♣3 的字符表示應為 '♣3'"""
        card = Card(3, 0)
        self.assertEqual(repr(card), "♣3")

    def test_card_compare_suit(self):
        """測試：♠ > ♥ 花色比較"""
        card1 = Card(14, 3)  # ♠A
        card2 = Card(14, 2)  # ♥A
        self.assertTrue(card1 > card2)

    def test_card_compare_suit_2(self):
        """測試：♥ > ♦ 花色比較"""
        card1 = Card(14, 2)  # ♥A
        card2 = Card(14, 1)  # ♦A
        self.assertTrue(card1 > card2)

    def test_card_compare_suit_3(self):
        """測試：♦ > ♣ 花色比較"""
        card1 = Card(14, 1)  # ♦A
        card2 = Card(14, 0)  # ♣A
        self.assertTrue(card1 > card2)

    def test_card_compare_rank_2(self):
        """測試：2 > A 點數比較"""
        card1 = Card(15, 0)  # 2♣
        card2 = Card(14, 3)  # ♠A
        self.assertTrue(card1 > card2)

    def test_card_compare_rank_a(self):
        """測試：A > K 點數比較"""
        card1 = Card(14, 0)  # ♣A
        card2 = Card(13, 3)  # ♠K
        self.assertTrue(card1 > card2)

    def test_card_compare_equal(self):
        """測試：相同的牌不應大於彼此"""
        card1 = Card(14, 3)
        card2 = Card(14, 3)
        self.assertFalse(card1 > card2)

    def test_card_sort_key(self):
        """測試：to_sort_key() 回傳正確元組"""
        card = Card(14, 3)
        self.assertEqual(card.to_sort_key(), (14, 3))


class TestDeck(unittest.TestCase):
    """Deck 類別的單元測試"""

    def test_deck_has_52_cards(self):
        """測試：牌堆初始時有 52 張牌"""
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_all_unique(self):
        """測試：牌堆中所有牌都是唯一的"""
        deck = Deck()
        # 轉成集合，應該還有 52 張（無重複）
        self.assertEqual(len(set(deck.cards)), 52)

    def test_deck_all_ranks(self):
        """測試：牌堆包含所有點數 (3-15)"""
        deck = Deck()
        ranks = set(card.rank for card in deck.cards)
        expected_ranks = set(range(3, 16))
        self.assertEqual(ranks, expected_ranks)

    def test_deck_all_suits(self):
        """測試：牌堆包含所有花色 (0,1,2,3)"""
        deck = Deck()
        suits = set(card.suit for card in deck.cards)
        expected_suits = {0, 1, 2, 3}
        self.assertEqual(suits, expected_suits)

    def test_deck_shuffle(self):
        """測試：洗牌後牌的順序改變"""
        deck = Deck()
        original_order = [card.to_sort_key() for card in deck.cards]
        deck.shuffle()
        shuffled_order = [card.to_sort_key() for card in deck.cards]
        # 洗牌後順序應該改變（概率極小不會相同）
        self.assertNotEqual(original_order, shuffled_order)

    def test_deal_5_cards(self):
        """測試：發 5 張牌後應剩 47 張"""
        deck = Deck()
        dealt = deck.deal(5)
        self.assertEqual(len(dealt), 5)
        self.assertEqual(len(deck.cards), 47)

    def test_deal_multiple(self):
        """測試：連續發牌"""
        deck = Deck()
        deck.deal(5)
        deck.deal(3)
        self.assertEqual(len(deck.cards), 44)

    def test_deal_exceed(self):
        """測試：要求發超過剩餘數量的牌"""
        deck = Deck()
        dealt = deck.deal(60)
        self.assertEqual(len(dealt), 52)
        self.assertEqual(len(deck.cards), 0)


class TestHand(unittest.TestCase):
    """Hand 類別的單元測試"""

    def test_hand_creation(self):
        """測試：建立 Hand 物件"""
        cards = [Card(3, 0), Card(14, 3), Card(5, 1)]
        hand = Hand(cards)
        self.assertEqual(len(hand), 3)

    def test_hand_sort_desc(self):
        """測試：手牌降序排列"""
        cards = [Card(3, 0), Card(14, 3), Card(13, 2), Card(14, 2)]
        hand = Hand(cards)
        hand.sort_desc()
        # 預期順序：按點數降序，同點數按花色升序
        # A 點數 14：花色 (0♣,1♦,2♥,3♠)
        # 所以 A♥ (14,2) 在 A♠ (14,3) 之前
        # 最後是 K♥ (13,2), 3♣ (3,0)
        expected_repr = ["♥A", "♠A", "♥K", "♣3"]
        actual_repr = [repr(card) for card in hand]
        self.assertEqual(actual_repr, expected_repr)

    def test_hand_find_3_clubs(self):
        """測試：找到 3♣"""
        cards = [Card(14, 3), Card(3, 0), Card(5, 1)]
        hand = Hand(cards)
        three_clubs = hand.find_3_clubs()
        self.assertIsNotNone(three_clubs)
        self.assertEqual(three_clubs.rank, 3)
        self.assertEqual(three_clubs.suit, 0)

    def test_hand_find_3_clubs_none(self):
        """測試：找不到 3♣ 時回傳 None"""
        cards = [Card(14, 3), Card(5, 1)]
        hand = Hand(cards)
        three_clubs = hand.find_3_clubs()
        self.assertIsNone(three_clubs)

    def test_hand_remove(self):
        """測試：移除指定的牌"""
        cards = [Card(14, 3), Card(3, 0), Card(5, 1)]
        hand = Hand(cards)
        hand.remove([Card(3, 0)])
        self.assertEqual(len(hand), 2)

    def test_hand_remove_not_found(self):
        """測試：移除不存在的牌，手牌數量不變"""
        cards = [Card(14, 3), Card(3, 0)]
        hand = Hand(cards)
        original_len = len(hand)
        hand.remove([Card(5, 1)])  # 不存在的牌
        self.assertEqual(len(hand), original_len)

    def test_hand_iteration(self):
        """測試：迭代手牌"""
        cards = [Card(14, 3), Card(3, 0)]
        hand = Hand(cards)
        hand_list = list(hand)
        self.assertEqual(len(hand_list), 2)


class TestPlayer(unittest.TestCase):
    """Player 類別的單元測試"""

    def test_player_human(self):
        """測試：建立人類玩家"""
        player = Player("Player1", False)
        self.assertEqual(player.name, "Player1")
        self.assertFalse(player.is_ai)

    def test_player_ai(self):
        """測試：建立 AI 玩家"""
        player = Player("AI_1", True)
        self.assertEqual(player.name, "AI_1")
        self.assertTrue(player.is_ai)

    def test_player_take(self):
        """測試：玩家拿牌"""
        player = Player("Player1", False)
        cards = [Card(14, 3), Card(3, 0)]
        player.take_cards(cards)
        self.assertEqual(len(player.hand), 2)

    def test_player_play(self):
        """測試：玩家出牌"""
        player = Player("Player1", False)
        cards = [Card(14, 3), Card(3, 0), Card(5, 1)]
        player.take_cards(cards)
        played = player.play_cards([Card(3, 0)])
        # 驗證回傳出牌
        self.assertEqual(len(played), 1)
        # 驗證手牌減少
        self.assertEqual(len(player.hand), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
