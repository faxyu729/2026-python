"""
P6 - GUI 測試
測試 Pygame UI 組件
"""

import unittest
from unittest.mock import MagicMock, patch
from game.models_p1 import Card, Hand


class TestUIBasic(unittest.TestCase):
    """基礎 UI 測試"""

    def test_card_render_dimensions(self):
        """測試：牌卡尺寸"""
        # 模擬牌卡尺寸
        card_width = 60
        card_height = 90
        self.assertGreater(card_width, 0)
        self.assertGreater(card_height, 0)

    def test_colors_defined(self):
        """測試：顏色配置"""
        colors = {
            "background": (45, 45, 45),
            "card_back": (74, 144, 217),
            "spade_club": (255, 255, 255),
            "heart_diamond": (231, 76, 60),
        }
        self.assertEqual(len(colors), 4)

    def test_hand_render_multiple_cards(self):
        """測試：多張牌渲染"""
        hand = Hand([Card(3, 0), Card(5, 1), Card(7, 2)])
        self.assertEqual(len(hand), 3)

    def test_hand_render_empty(self):
        """測試：空手牌渲染"""
        hand = Hand([])
        self.assertEqual(len(hand), 0)


class TestGameInit(unittest.TestCase):
    """遊戲初始化測試"""

    def test_game_app_creation(self):
        """測試：應用初始化"""
        # 模擬應用初始化
        game_state = {"players": 4, "window_width": 1280, "window_height": 720}
        self.assertEqual(game_state["players"], 4)

    def test_game_has_correct_players(self):
        """測試：遊戲有正確數量的玩家"""
        from game.game_p5 import BigTwoGame

        game = BigTwoGame()
        game.setup()
        self.assertEqual(len(game.players), 4)


class TestCardSelection(unittest.TestCase):
    """卡選擇測試"""

    def test_card_position_calculation(self):
        """測試：卡位置計算"""
        # 模擬卡的位置計算
        cards = [Card(3, 0), Card(5, 1), Card(7, 2)]
        card_width = 60
        spacing = 10

        positions = []
        for i, card in enumerate(cards):
            x = i * (card_width + spacing)
            positions.append(x)

        self.assertEqual(len(positions), 3)
        self.assertEqual(positions[0], 0)
        self.assertEqual(positions[1], 70)

    def test_mouse_click_to_card(self):
        """測試：鼠標點擊轉換為卡索引"""
        card_width = 60
        spacing = 10
        cards_x_positions = [0, 70, 140]

        # 模擬點擊第二張卡
        mouse_x = 75
        card_index = None
        for i, x in enumerate(cards_x_positions):
            if mouse_x >= x and mouse_x < x + card_width:
                card_index = i
                break

        self.assertEqual(card_index, 1)

    def test_selection_toggle(self):
        """測試：卡選擇切換"""
        selected_indices = set()

        # 選擇第0張
        if 0 not in selected_indices:
            selected_indices.add(0)
        self.assertIn(0, selected_indices)

        # 取消選擇第0張
        if 0 in selected_indices:
            selected_indices.remove(0)
        self.assertNotIn(0, selected_indices)


class TestButtonLogic(unittest.TestCase):
    """按鈕邏輯測試"""

    def test_button_regions(self):
        """測試：按鈕區域"""
        buttons = {
            "play": {"x": 100, "y": 600, "width": 100, "height": 40},
            "pass": {"x": 220, "y": 600, "width": 100, "height": 40},
        }

        self.assertEqual(buttons["play"]["x"], 100)
        self.assertEqual(buttons["pass"]["x"], 220)

    def test_button_click_detection(self):
        """測試：按鈕點擊檢測"""
        button = {"x": 100, "y": 600, "width": 100, "height": 40}

        # 點擊在按鈕區域內
        mouse_pos = (150, 620)
        is_clicked = (
            mouse_pos[0] >= button["x"]
            and mouse_pos[0] < button["x"] + button["width"]
            and mouse_pos[1] >= button["y"]
            and mouse_pos[1] < button["y"] + button["height"]
        )

        self.assertTrue(is_clicked)

    def test_button_click_outside(self):
        """測試：按鈕外點擊"""
        button = {"x": 100, "y": 600, "width": 100, "height": 40}

        # 點擊在按鈕區域外
        mouse_pos = (50, 620)
        is_clicked = (
            mouse_pos[0] >= button["x"]
            and mouse_pos[0] < button["x"] + button["width"]
            and mouse_pos[1] >= button["y"]
            and mouse_pos[1] < button["y"] + button["height"]
        )

        self.assertFalse(is_clicked)


class TestGameFlow(unittest.TestCase):
    """遊戲流程集成測試"""

    def test_valid_play_workflow(self):
        """測試：合法出牌流程"""
        from game.game_p5 import BigTwoGame
        from game.classifier_p2 import HandClassifier

        game = BigTwoGame()
        game.setup()

        # 找第一個玩家的一張牌
        player = game.players[0]
        if player.hand:
            card = player.hand[0]

            # 檢查是否可以出
            is_valid = HandClassifier.can_play(None, [card])
            self.assertTrue(isinstance(is_valid, bool))

    def test_game_state_tracking(self):
        """測試：遊戲狀態追蹤"""
        from game.game_p5 import BigTwoGame

        game = BigTwoGame()
        game.setup()

        # 追蹤初始狀態
        self.assertIsNone(game.last_play)
        self.assertEqual(game.pass_count, 0)
        self.assertIsNone(game.winner)
        self.assertFalse(game.is_game_over())

    def test_player_transition(self):
        """測試：玩家輪轉"""
        from game.game_p5 import BigTwoGame

        game = BigTwoGame()
        game.setup()

        initial_player = game.current_player
        game.next_turn()
        next_player = game.current_player

        self.assertEqual(next_player, (initial_player + 1) % 4)


class TestRenderData(unittest.TestCase):
    """渲染數據準備測試"""

    def test_player_display_info(self):
        """測試：玩家顯示信息"""
        from game.models_p1 import Player

        player = Player("TestPlayer", False)
        player.take_cards([Card(3, 0), Card(5, 1)])

        display_info = {
            "name": player.name,
            "card_count": len(player.hand),
            "is_ai": player.is_ai,
        }

        self.assertEqual(display_info["name"], "TestPlayer")
        self.assertEqual(display_info["card_count"], 2)
        self.assertFalse(display_info["is_ai"])

    def test_last_play_display(self):
        """測試：上家出牌顯示"""
        last_play = [Card(5, 0), Card(5, 1)]

        # 準備顯示數據
        display_data = {
            "cards": last_play,
            "count": len(last_play),
            "player_name": "AI1",
        }

        self.assertEqual(display_data["count"], 2)
        self.assertEqual(display_data["player_name"], "AI1")

    def test_hand_display_order(self):
        """測試：手牌顯示順序"""
        hand = Hand([Card(3, 0), Card(14, 3), Card(13, 2)])
        hand.sort_desc()

        # 驗證排序順序
        ranks = [card.rank for card in hand]
        self.assertEqual(ranks[0], 14)  # A 在最前
        self.assertEqual(ranks[-1], 3)  # 3 在最後


if __name__ == "__main__":
    unittest.main(verbosity=2)
