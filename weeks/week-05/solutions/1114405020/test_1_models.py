import unittest
from game.models import Card, Deck, Hand, Player


class TestCard(unittest.TestCase):
    """測試Card卡牌類別"""

    def test_card_creation(self):
        """測試1: 卡牌建立"""
        card = Card(rank=14, suit=3)
        self.assertEqual(card.rank, 14)
        self.assertEqual(card.suit, 3)

    def test_card_repr_ace(self):
        """測試2: Ace卡牌的字符串表示（♠A）"""
        card = Card(14, 3)
        self.assertEqual(repr(card), "♠A")

    def test_card_repr_three(self):
        """測試3: 數字3卡牌的字符串表示（♣3）"""
        card = Card(3, 0)
        self.assertEqual(repr(card), "♣3")

    def test_card_compare_suit(self):
        """測試4: 同數字比花色（♠>♥）"""
        card1 = Card(14, 3)  # ♠A
        card2 = Card(14, 2)  # ♥A
        self.assertTrue(card1 > card2)

    def test_card_compare_suit_2(self):
        """測試5: 同數字比花色（♥>♦）"""
        card1 = Card(14, 2)  # ♥A
        card2 = Card(14, 1)  # ♦A
        self.assertTrue(card1 > card2)

    def test_card_compare_suit_3(self):
        """測試6: 同數字比花色（♦>♣）"""
        card1 = Card(14, 1)  # ♦A
        card2 = Card(14, 0)  # ♣A
        self.assertTrue(card1 > card2)

    def test_card_compare_rank_2(self):
        """測試7: 不同數字比較（2>A）"""
        card1 = Card(15, 0)  # ♣2
        card2 = Card(14, 3)  # ♠A
        self.assertTrue(card1 > card2)

    def test_card_compare_rank_a(self):
        """測試8: 不同數字比較（A>K）"""
        card1 = Card(14, 0)  # ♣A
        card2 = Card(13, 3)  # ♠K
        self.assertTrue(card1 > card2)

    def test_card_compare_equal(self):
        """測試9: 相同卡牌比較"""
        card1 = Card(14, 3)  # ♠A
        card2 = Card(14, 3)  # ♠A
        self.assertFalse(card1 > card2)
        self.assertTrue(card1 == card2)

    def test_card_sort_key(self):
        """測試10: 卡牌排序鍵"""
        card = Card(14, 3)
        self.assertEqual(card.to_sort_key(), (14, 3))


class TestDeck(unittest.TestCase):
    """測試Deck牌組類別"""

    def test_deck_has_52_cards(self):
        """測試11: 牌組包含52張牌"""
        deck = Deck()
        self.assertEqual(len(deck), 52)

    def test_deck_all_unique(self):
        """測試12: 所有牌都不重複"""
        deck = Deck()
        cards_set = set(deck.cards)
        self.assertEqual(len(cards_set), 52)

    def test_deck_all_ranks(self):
        """測試13: 包含所有的數字（3-14及15）"""
        deck = Deck()
        ranks = set(card.rank for card in deck.cards)
        expected_ranks = set(list(range(3, 15)) + [15])
        self.assertEqual(ranks, expected_ranks)

    def test_deck_all_suits(self):
        """測試14: 包含所有4種花色"""
        deck = Deck()
        suits = set(card.suit for card in deck.cards)
        self.assertEqual(suits, {0, 1, 2, 3})

    def test_deck_shuffle(self):
        """測試15: 洗牌改變牌序"""
        deck1 = Deck()
        original_order = [str(card) for card in deck1.cards]

        deck1.shuffle()
        shuffled_order = [str(card) for card in deck1.cards]

        # 由於洗牌是隨機的，理論上不會完全相同（實際上99.9%不會）
        # 但我們檢查至少有一些改變
        self.assertNotEqual(original_order, shuffled_order)

    def test_deal_5_cards(self):
        """測試16: 發5張牌後，牌組剩47張"""
        deck = Deck()
        dealt = deck.deal(5)

        self.assertEqual(len(dealt), 5)
        self.assertEqual(len(deck), 47)

    def test_deal_multiple(self):
        """測試17: 連續發牌"""
        deck = Deck()
        deck.deal(5)  # 第一次發5張
        deck.deal(3)  # 第二次發3張

        self.assertEqual(len(deck), 44)

    def test_deal_exceed(self):
        """測試18: 要求的牌數超過牌組時，返回全部牌"""
        deck = Deck()
        dealt = deck.deal(60)

        self.assertEqual(len(dealt), 52)
        self.assertEqual(len(deck), 0)


class TestHand(unittest.TestCase):
    """測試Hand手牌類別"""

    def test_hand_creation(self):
        """測試19: 手牌建立"""
        cards = [Card(3, 0), Card(4, 0), Card(5, 0)]
        hand = Hand(cards)
        self.assertEqual(len(hand), 3)

    def test_hand_sort_desc(self):
        """測試20: 手牌降序排序"""
        # 建立手牌：♣3, ♠A, ♦3, ♥K
        cards = [
            Card(3, 0),  # ♣3
            Card(14, 3),  # ♠A
            Card(3, 1),  # ♦3
            Card(13, 2),  # ♥K
        ]
        hand = Hand(cards)
        hand.sort_desc()

        # 驗證排序結果：♠A > ♥K > ♦3 > ♣3
        self.assertEqual(hand[0], Card(14, 3))  # ♠A
        self.assertEqual(hand[1], Card(13, 2))  # ♥K
        self.assertEqual(hand[2], Card(3, 1))  # ♦3
        self.assertEqual(hand[3], Card(3, 0))  # ♣3

    def test_hand_find_3_clubs(self):
        """測試21: 在手牌中查找♣3"""
        cards = [Card(14, 3), Card(3, 0), Card(3, 1)]
        hand = Hand(cards)

        found = hand.find_3_clubs()
        self.assertIsNotNone(found)
        self.assertEqual(found, Card(3, 0))

    def test_hand_find_3_clubs_none(self):
        """測試22: 查找不存在的牌返回None"""
        cards = [Card(14, 3), Card(3, 1)]
        hand = Hand(cards)

        found = hand.find_3_clubs()
        self.assertIsNone(found)

    def test_hand_remove(self):
        """測試23: 移除指定的牌"""
        cards = [Card(14, 3), Card(3, 0), Card(3, 1)]
        hand = Hand(cards)

        hand.remove([Card(3, 0)])

        self.assertEqual(len(hand), 2)

    def test_hand_remove_not_found(self):
        """測試24: 移除不存在的牌時，手牌數量不變"""
        cards = [Card(14, 3), Card(3, 1)]
        hand = Hand(cards)

        hand.remove([Card(3, 0)])

        self.assertEqual(len(hand), 2)

    def test_hand_iteration(self):
        """測試25: 手牌支持迭代"""
        cards = [Card(14, 3), Card(3, 0)]
        hand = Hand(cards)

        card_list = list(hand)
        self.assertEqual(len(card_list), 2)
        self.assertIn(Card(14, 3), card_list)


class TestPlayer(unittest.TestCase):
    """測試Player玩家類別"""

    def test_player_human(self):
        """測試26: 人類玩家建立"""
        player = Player("Player1", is_ai=False)

        self.assertEqual(player.name, "Player1")
        self.assertFalse(player.is_ai)

    def test_player_ai(self):
        """測試27: AI玩家建立"""
        player = Player("AI_1", is_ai=True)

        self.assertEqual(player.name, "AI_1")
        self.assertTrue(player.is_ai)

    def test_player_take(self):
        """測試28: 玩家接收卡牌"""
        player = Player("Player1", is_ai=False)
        cards = [Card(3, 0), Card(4, 0)]

        player.take_cards(cards)

        self.assertEqual(len(player.hand), 2)

    def test_player_play(self):
        """測試29: 玩家出牌"""
        player = Player("Player1", is_ai=False)
        cards = [Card(3, 0), Card(4, 0), Card(5, 0)]
        player.take_cards(cards)

        # 出牌
        played = player.play_cards([Card(3, 0), Card(4, 0)])

        self.assertEqual(len(played), 2)
        self.assertEqual(len(player.hand), 1)
        self.assertIn(Card(5, 0), player.hand)


if __name__ == "__main__":
    unittest.main(verbosity=2)
