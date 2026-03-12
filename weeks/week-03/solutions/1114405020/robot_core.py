"""Robot Lost 核心邏輯。

本模組刻意不依賴 pygame，讓規則可以被 unittest 快速驗證。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

# 方向順序用於旋轉運算：往右是 +1，往左是 -1。
DIRECTIONS = ("N", "E", "S", "W")
VALID_COMMANDS = {"L", "R", "F"}
MOVE_TABLE = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}

# scent 的資料型別：最後安全位置 + 當下方向。
Scent = tuple[int, int, str]


@dataclass(frozen=True)
class RobotState:
    """機器人的單一快照狀態。"""

    x: int
    y: int
    direction: str
    lost: bool = False


class InvalidDirectionError(ValueError):
    """方向字元不合法。"""


def _validate_direction(direction: str) -> None:
    if direction not in DIRECTIONS:
        raise InvalidDirectionError(f"Invalid direction: {direction}")


def turn_left(direction: str) -> str:
    """方向左轉 90 度。"""
    _validate_direction(direction)
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx - 1) % 4]


def turn_right(direction: str) -> str:
    """方向右轉 90 度。"""
    _validate_direction(direction)
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx + 1) % 4]


def is_out_of_bounds(x: int, y: int, width: int, height: int) -> bool:
    """判斷座標是否超出邊界（邊界本身算合法）。"""
    return x < 0 or y < 0 or x > width or y > height


def apply_command(
    state: RobotState,
    command: str,
    width: int,
    height: int,
    scents: set[Scent],
    *,
    invalid_policy: str = "raise",
) -> RobotState:
    """執行單一步指令並回傳新狀態。

    invalid_policy:
    - "raise": 非法指令直接丟 ValueError
    - "ignore": 非法指令忽略，不改變狀態
    """
    if state.lost:
        return state

    if command not in VALID_COMMANDS:
        if invalid_policy == "ignore":
            return state
        raise ValueError(f"Invalid command: {command}")

    if command == "L":
        return RobotState(state.x, state.y, turn_left(state.direction), False)

    if command == "R":
        return RobotState(state.x, state.y, turn_right(state.direction), False)

    # command == "F"
    dx, dy = MOVE_TABLE[state.direction]
    next_x = state.x + dx
    next_y = state.y + dy

    if not is_out_of_bounds(next_x, next_y, width, height):
        return RobotState(next_x, next_y, state.direction, False)

    scent_key: Scent = (state.x, state.y, state.direction)
    if scent_key in scents:
        # 有同樣 scent，忽略這次危險前進。
        return state

    # 首次在此方向墜落，留下 scent 並 LOST。
    scents.add(scent_key)
    return RobotState(state.x, state.y, state.direction, True)


def run_commands(
    initial_state: RobotState,
    commands: Iterable[str],
    width: int,
    height: int,
    scents: set[Scent],
    *,
    invalid_policy: str = "raise",
) -> RobotState:
    """依序執行整串指令，遇到 LOST 立即停止。"""
    state = initial_state
    for command in commands:
        state = apply_command(
            state,
            command,
            width,
            height,
            scents,
            invalid_policy=invalid_policy,
        )
        if state.lost:
            break
    return state


def robot_to_output(state: RobotState) -> str:
    """輸出格式與 UVA 118 一致。"""
    suffix = " LOST" if state.lost else ""
    return f"{state.x} {state.y} {state.direction}{suffix}"
