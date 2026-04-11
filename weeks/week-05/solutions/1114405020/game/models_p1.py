"""
P1 - 資料模型
實現 Card、Deck、Hand、Player 四個基礎類別
"""

from itertools import combinations
import random


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
