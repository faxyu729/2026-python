# UI Input Handler
# Handles mouse and keyboard input


class InputHandler:
    """Input handler"""

    def __init__(self, renderer):
        """Initialize input handler"""
        self.renderer = renderer
        self.selected_indices = set()
        self.buttons = {
            "play": {"x": 650, "y": 475, "width": 80, "height": 35, "text": "出牌"},
            "pass": {"x": 750, "y": 475, "width": 80, "height": 35, "text": "過牌"},
        }
        self.button_rects = {}

    def set_button_rect(self, name, rect):
        """Set button rect"""
        self.button_rects[name] = rect

    def handle_click(self, pos, game):
        """Handle mouse click"""
        x, y = pos

        for button_name, rect in self.button_rects.items():
            if rect.collidepoint(x, y):
                if button_name == "play":
                    return self.try_play(game)
                elif button_name == "pass":
                    player = game.get_current_player()
                    game.pass_(player)
                    game.next_turn()
                    return True

        # 檢查卡牌點擊 - 手牌在 y > 280 的區域
        if y > 280 and y < 380:
            current_player = game.get_current_player()
            if not current_player.is_ai:
                card_width = self.renderer.CARD_WIDTH
                spacing = self.renderer.CARD_SPACING
                hand_size = len(current_player.hand)
                total_width = hand_size * card_width + (hand_size - 1) * spacing
                hand_start_x = (1100 - total_width) // 2  # 1100 是新窗口寬度

                for i in range(hand_size):
                    card_x = hand_start_x + i * (card_width + spacing)
                    if x >= card_x and x < card_x + card_width:
                        if i in self.selected_indices:
                            self.selected_indices.remove(i)
                        else:
                            self.selected_indices.add(i)
                        return True

        return False

    def handle_key(self, key, game):
        """Handle keyboard input"""
        import pygame

        if key == pygame.K_RETURN:
            return self.try_play(game)

        if key == pygame.K_p:
            player = game.get_current_player()
            game.pass_(player)
            game.next_turn()
            return True

        return False

    def try_play(self, game):
        """Try to play selected cards"""
        if not self.selected_indices:
            return False

        player = game.get_current_player()
        selected_cards = [player.hand[i] for i in sorted(self.selected_indices)]

        if game.play(player, selected_cards):
            self.selected_indices.clear()
            game.next_turn()
            return True

        return False

    def clear_selection(self):
        """Clear card selection"""
        self.selected_indices.clear()
