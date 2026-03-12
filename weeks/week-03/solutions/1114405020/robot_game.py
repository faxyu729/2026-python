"""Robot Lost pygame 互動版。

操作鍵：
- L / R / F: 執行一步指令
- N: 建立新機器人（保留 scent）
- C: 清除 scent
- B: 回放歷史軌跡
- G: 匯出 replay.gif
- P: 儲存目前畫面到 assets/gameplay.png
- ESC: 離開
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tempfile

import pygame

from robot_core import RobotState, Scent, apply_command


WIDTH = 5
HEIGHT = 3
CELL_SIZE = 90
PADDING = 40
HUD_HEIGHT = 230
WINDOW_WIDTH = (WIDTH + 1) * CELL_SIZE + PADDING * 2
WINDOW_HEIGHT = (HEIGHT + 1) * CELL_SIZE + PADDING * 2 + HUD_HEIGHT

BG_TOP = (245, 235, 219)
BG_BOTTOM = (226, 209, 186)
GRID_LINE = (88, 70, 52)
ROBOT_COLOR = (43, 79, 120)
SCENT_COLOR = (185, 72, 46)
TEXT_COLOR = (28, 27, 24)
OK_COLOR = (17, 117, 71)
WARN_COLOR = (165, 50, 42)


@dataclass
class FrameState:
    robot: RobotState
    scents: set[Scent]
    action: str
    status: str


class RobotLostGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Week03 Robot Lost - pygame")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # 優先使用繁中系統字型，讓 HUD 中文提示可直接閱讀。
        self.font = pygame.font.SysFont("Microsoft JhengHei", 24)
        self.small_font = pygame.font.SysFont("Microsoft JhengHei", 18)
        self.scents: set[Scent] = set()
        self.robot = RobotState(0, 0, "N", False)
        self.status_message = "新機器人已就緒：0,0,N"
        self.command_history: list[str] = []

        self.replay_index = 0
        self.replay_mode = False
        self.replay_tick = 0
        self.replay_speed = 18
        self.frames: list[FrameState] = []

        self._append_frame(action="INIT", status=self.status_message)

    def _append_frame(self, action: str, status: str) -> None:
        self.frames.append(
            FrameState(
                robot=self.robot,
                scents=set(self.scents),
                action=action,
                status=status,
            )
        )

    def _grid_to_pixel(self, x: int, y: int) -> tuple[int, int]:
        px = PADDING + x * CELL_SIZE + CELL_SIZE // 2
        py = PADDING + (HEIGHT - y) * CELL_SIZE + CELL_SIZE // 2
        return px, py

    def _draw_gradient_background(self) -> None:
        # 手動畫漸層，避免畫面看起來像純色底。
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
            g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
            b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def _draw_grid(self) -> None:
        for x in range(WIDTH + 1):
            for y in range(HEIGHT + 1):
                left = PADDING + x * CELL_SIZE
                top = PADDING + (HEIGHT - y) * CELL_SIZE
                rect = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (252, 249, 243), rect)
                pygame.draw.rect(self.screen, GRID_LINE, rect, 2)

    def _draw_scents(self, scents: set[Scent]) -> None:
        for sx, sy, sdir in sorted(scents):
            px, py = self._grid_to_pixel(sx, sy)
            pygame.draw.circle(self.screen, SCENT_COLOR, (px, py), 9)
            label = self.small_font.render(sdir, True, (255, 248, 240))
            label_rect = label.get_rect(center=(px, py))
            self.screen.blit(label, label_rect)

    def _robot_triangle(self, state: RobotState) -> list[tuple[int, int]]:
        px, py = self._grid_to_pixel(state.x, state.y)
        s = 25
        if state.direction == "N":
            return [(px, py - s), (px - s + 4, py + s - 2), (px + s - 4, py + s - 2)]
        if state.direction == "E":
            return [(px + s, py), (px - s + 2, py - s + 4), (px - s + 2, py + s - 4)]
        if state.direction == "S":
            return [(px, py + s), (px - s + 4, py - s + 2), (px + s - 4, py - s + 2)]
        return [(px - s, py), (px + s - 2, py - s + 4), (px + s - 2, py + s - 4)]

    def _draw_robot(self, state: RobotState) -> None:
        points = self._robot_triangle(state)
        color = WARN_COLOR if state.lost else ROBOT_COLOR
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, (250, 248, 241), points, 2)

    def _draw_hud(self, state: RobotState, scents: set[Scent], status: str, action: str) -> None:
        hud_top = PADDING + (HEIGHT + 1) * CELL_SIZE + 10
        hud_rect = pygame.Rect(PADDING, hud_top, WINDOW_WIDTH - PADDING * 2, HUD_HEIGHT - 20)
        pygame.draw.rect(self.screen, (246, 241, 229), hud_rect, border_radius=12)
        pygame.draw.rect(self.screen, (107, 87, 63), hud_rect, 2, border_radius=12)

        left_x = hud_rect.x + 16

        title = self.font.render("Robot Lost 規則模擬", True, TEXT_COLOR)
        self.screen.blit(title, (left_x, hud_rect.y + 12))

        robot_text = f"機器人: ({state.x}, {state.y}) {state.direction} | {'LOST' if state.lost else 'ALIVE'}"
        scent_text = f"scent 數量: {len(scents)} | 歷程步數: {len(self.frames) - 1}"
        action_text = f"最近操作: {action}"

        self.screen.blit(self.small_font.render(robot_text, True, TEXT_COLOR), (left_x, hud_rect.y + 50))
        self.screen.blit(self.small_font.render(scent_text, True, TEXT_COLOR), (left_x, hud_rect.y + 76))
        self.screen.blit(self.small_font.render(action_text, True, TEXT_COLOR), (left_x, hud_rect.y + 102))

        status_color = WARN_COLOR if "LOST" in status else OK_COLOR
        self.screen.blit(self.small_font.render(status, True, status_color), (left_x, hud_rect.y + 128))

        controls_line_1 = "L/R/F 單步 | N 新機器人 | C 清 scent"
        controls_line_2 = "B 回放 | G 匯出 GIF | P 截圖 | ESC 離開"
        self.screen.blit(self.small_font.render(controls_line_1, True, TEXT_COLOR), (left_x, hud_rect.y + 154))
        self.screen.blit(self.small_font.render(controls_line_2, True, TEXT_COLOR), (left_x, hud_rect.y + 178))

    def _draw_scene(self, state: RobotState, scents: set[Scent], status: str, action: str) -> None:
        self._draw_gradient_background()
        self._draw_grid()
        self._draw_scents(scents)
        self._draw_robot(state)
        self._draw_hud(state, scents, status, action)

    def handle_command(self, cmd: str) -> None:
        if self.robot.lost:
            self.status_message = "此機器人已 LOST，請按 N 建立新機器人"
            self._append_frame(action=cmd, status=self.status_message)
            return

        self.robot = apply_command(self.robot, cmd, WIDTH, HEIGHT, self.scents)
        self.command_history.append(cmd)

        if self.robot.lost:
            self.status_message = f"執行 {cmd} 後 LOST，已留下 scent"
        else:
            self.status_message = f"執行 {cmd} 成功"

        self._append_frame(action=cmd, status=self.status_message)

    def new_robot(self) -> None:
        # 這裡固定從 0,0,N 重新出發，方便課堂展示 scent 累積效果。
        self.robot = RobotState(0, 0, "N", False)
        self.status_message = "新機器人建立完成（保留既有 scent）"
        self._append_frame(action="N", status=self.status_message)

    def clear_scents(self) -> None:
        self.scents.clear()
        self.status_message = "已清除所有 scent"
        self._append_frame(action="C", status=self.status_message)

    def toggle_replay(self) -> None:
        if len(self.frames) <= 1:
            self.status_message = "目前沒有可回放的歷程"
            return
        self.replay_mode = not self.replay_mode
        self.replay_index = 0
        self.replay_tick = 0
        self.status_message = "回放模式啟用" if self.replay_mode else "回放模式關閉"

    def export_gif(self) -> None:
        """將歷程輸出為 assets/replay.gif（需要 Pillow）。"""
        if len(self.frames) <= 1:
            self.status_message = "沒有足夠的歷程可匯出 GIF"
            return

        try:
            from PIL import Image
        except ImportError:
            self.status_message = "尚未安裝 Pillow，請先 pip install Pillow"
            return

        output_path = Path(__file__).resolve().parent / "assets" / "replay.gif"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmp:
            image_paths: list[Path] = []
            surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            for idx, frame in enumerate(self.frames):
                # 用同一套繪圖流程把每個 frame 轉成圖片。
                self.screen = surface
                self._draw_scene(frame.robot, frame.scents, frame.status, frame.action)
                temp_path = Path(tmp) / f"frame_{idx:04d}.png"
                pygame.image.save(surface, str(temp_path))
                image_paths.append(temp_path)

            # 還原主畫布，避免匯出後畫面失效。
            self.screen = pygame.display.get_surface()

            images = [Image.open(p).convert("P", palette=Image.ADAPTIVE) for p in image_paths]
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                duration=180,
                loop=0,
            )

        self.status_message = f"已匯出 GIF: {output_path.name}"

    def save_gameplay_screenshot(self) -> None:
        """儲存目前畫面到 assets/gameplay.png，方便作業提交。"""
        output_path = Path(__file__).resolve().parent / "assets" / "gameplay.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 先重繪一幀，確保截圖含最新狀態與 HUD。
        self._draw_scene(self.robot, self.scents, self.status_message, "LIVE")
        pygame.display.flip()
        pygame.image.save(self.screen, str(output_path))
        self.status_message = f"已儲存截圖: {output_path.name}"

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_l:
                        self.handle_command("L")
                    elif event.key == pygame.K_r:
                        self.handle_command("R")
                    elif event.key == pygame.K_f:
                        self.handle_command("F")
                    elif event.key == pygame.K_n:
                        self.new_robot()
                    elif event.key == pygame.K_c:
                        self.clear_scents()
                    elif event.key == pygame.K_b:
                        self.toggle_replay()
                    elif event.key == pygame.K_g:
                        self.export_gif()
                    elif event.key == pygame.K_p:
                        self.save_gameplay_screenshot()

            if self.replay_mode and self.frames:
                self.replay_tick += 1
                if self.replay_tick >= self.replay_speed:
                    self.replay_tick = 0
                    self.replay_index += 1
                    if self.replay_index >= len(self.frames):
                        self.replay_index = 0

                frame = self.frames[self.replay_index]
                self._draw_scene(frame.robot, frame.scents, frame.status, f"REPLAY:{frame.action}")
            else:
                self._draw_scene(self.robot, self.scents, self.status_message, "LIVE")

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    RobotLostGame().run()
