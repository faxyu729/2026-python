# UI Renderer
# Handles all game rendering

import pygame
import os


class Renderer:
    """Game renderer"""

    # Color configuration
    COLORS = {
        "background": (108, 142, 168),  # 藍灰色
        "card_white": (255, 255, 255),
        "text": (255, 255, 255),
        "text_dark": (0, 0, 0),
        "current_player": (255, 215, 0),
        "button": (70, 130, 180),
    }

    # Card sizes
    CARD_WIDTH = 70
    CARD_HEIGHT = 100

    def __init__(self):
        """Initialize renderer"""
        # 使用 pygame 內置字體
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 18)
        self.font_small = pygame.font.Font(None, 14)

    def render_text(self, text: str, size: int, color: tuple) -> pygame.Surface:
        """Render text using pygame font"""
        try:
            # 根據 size 選擇適當的字體
            if size >= 20:
                font = pygame.font.Font(None, size)
            elif size >= 12:
                font = pygame.font.Font(None, size)
            else:
                font = pygame.font.Font(None, size)

            # 用 pygame 字體渲染（只支持 ASCII）
            # 將中文轉換為 ASCII 等價物或符號
            display_text = self._convert_text_for_display(text)
            return font.render(display_text, True, color)
        except Exception as e:
            print(f"Text rendering error: {e}")
            # 返回空 Surface
            return pygame.Surface((1, 1))

    def _convert_text_for_display(self, text: str) -> str:
        """Convert Chinese text to ASCII-compatible display text"""
        # 對於遊戲規則等，直接返回原文本（pygame 會顯示為方塊或符號）
        # 我們只需要確保花色符號能顯示
        return text

    def draw_card(self, screen, card, x, y, selected=False, small=False):
        """Draw a single card"""
        w = self.CARD_WIDTH
        h = self.CARD_HEIGHT

        if selected:
            bg_color = (150, 200, 255)  # 淺藍色
        else:
            bg_color = self.COLORS["card_white"]

        # 背景
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, bg_color, rect)

        # 花色映射 - 用簡單的文本代替
        suit_text_map = {
            0: "C",
            1: "D",
            2: "H",
            3: "S",
        }  # C=Clubs, D=Diamonds, H=Hearts, S=Spades

        # 點數映射
        rank_symbols = {
            2: "3",
            3: "4",
            4: "5",
            5: "6",
            6: "7",
            7: "8",
            8: "9",
            9: "10",
            10: "J",
            11: "Q",
            12: "K",
            13: "A",
            14: "A",
            15: "2",
        }

        suit_sym = suit_text_map.get(card.suit, "?")
        rank_sym = rank_symbols.get(card.rank, "?")

        # 花色顏色
        if card.suit in [1, 2]:  # 鑽石、紅心
            suit_color = (255, 0, 0)  # 紅色
        else:  # 梅花、黑桃
            suit_color = (0, 0, 0)  # 黑色

        # 渲染花色符號
        suit_font = pygame.font.Font(None, 32)
        suit_surf = suit_font.render(suit_sym, True, suit_color)
        suit_rect = suit_surf.get_rect(center=(x + w // 2, y + h // 3))
        screen.blit(suit_surf, suit_rect)

        # 渲染點數
        rank_font = pygame.font.Font(None, 18)
        rank_surf = rank_font.render(rank_sym, True, (0, 0, 0))
        rank_rect = rank_surf.get_rect(center=(x + w // 2, y + 2 * h // 3))
        screen.blit(rank_surf, rank_rect)

    def draw_hand(self, screen, hand, x, y, selected_indices):
        """Draw player's hand"""
        for i, card in enumerate(hand):
            card_x = x + i * (self.CARD_WIDTH + 10)
            is_selected = i in selected_indices
            self.draw_card(screen, card, card_x, y, selected=is_selected)


class InputHandler:
    """Input handler"""

    def __init__(self, renderer):
        """Initialize input handler"""
        self.renderer = renderer
        self.card_width = renderer.CARD_WIDTH
        self.card_height = renderer.CARD_HEIGHT
        self.hand_y = 410

    def handle_click(self, pos, game):
        """Handle mouse click"""
        x, y = pos

        # 檢查是否點擊了卡牌
        hand = game.players[0].hand
        for i, card in enumerate(hand):
            card_x = 180 + i * 72
            card_rect = pygame.Rect(
                card_x, self.hand_y, self.card_width, self.card_height
            )
            if card_rect.collidepoint(x, y):
                return {"selected_cards": [card]}

        # 檢查是否點擊了按鈕
        button_y = 510 - 40

        # 出牌按鈕
        if pygame.Rect(240, button_y, 120, 35).collidepoint(x, y):
            return "play"

        # 過牌按鈕
        if pygame.Rect(380, button_y, 120, 35).collidepoint(x, y):
            return "pass"

        # 重新開始按鈕
        if pygame.Rect(530, button_y, 120, 35).collidepoint(x, y):
            return "restart"

        return None
