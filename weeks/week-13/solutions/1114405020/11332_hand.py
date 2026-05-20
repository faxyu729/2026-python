# -*- coding: utf-8 -*-
"""
UVA 11332 — 鏡子可見性（手打程式）

題目：原點 (0,0) 處有觀察者，四周有 n 條線段（鏡子）。
      對每條鏡子，判斷是否能從原點看到至少一部份區域。
"""

def cross(ax, ay, bx, by):
    """計算向量叉積"""
    return ax * by - ay * bx


def on_segment(px, py, qx, qy, rx, ry):
    """檢查點 R 是否在線段 PQ 上"""
    return (min(px, qx) <= rx <= max(px, qx) and
            min(py, qy) <= ry <= max(py, qy))


def segments_intersect(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y):
    """檢查線段 P1-P2 與線段 P3-P4 是否相交"""
    d1 = cross(p2x - p1x, p2y - p1y, p3x - p1x, p3y - p1y)
    d2 = cross(p2x - p1x, p2y - p1y, p4x - p1x, p4y - p1y)
    d3 = cross(p4x - p3x, p4y - p3y, p1x - p3x, p1y - p3y)
    d4 = cross(p4x - p3x, p4y - p3y, p2x - p3x, p2y - p3y)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    if d1 == 0 and on_segment(p3x, p3y, p4x, p4y, p1x, p1y):
        return True
    if d2 == 0 and on_segment(p3x, p3y, p4x, p4y, p2x, p2y):
        return True
    if d3 == 0 and on_segment(p1x, p1y, p2x, p2y, p3x, p3y):
        return True
    if d4 == 0 and on_segment(p1x, p1y, p2x, p2y, p4x, p4y):
        return True
    return False


def point_distance_sq(px, py, qx, qy):
    """計算兩點距離的平方"""
    return (px - qx) ** 2 + (py - qy) ** 2


def is_visible_from_origin(sx, sy, ex, ey, mirrors, idx):
    """檢查第 idx 個鏡子是否能從原點看到（採樣 10 個點）"""
    num_samples = 10
    for t_int in range(num_samples + 1):
        t = t_int / num_samples
        px = sx + t * (ex - sx)
        py = sy + t * (ey - sy)
        if px == 0 and py == 0:
            continue
        blocked = False
        for j, (jx1, jy1, jx2, jy2) in enumerate(mirrors):
            if j == idx:
                continue
            if segments_intersect(0, 0, px, py, jx1, jy1, jx2, jy2):
                if point_distance_sq(0, 0, jx1, jy1) < point_distance_sq(0, 0, px, py) or \
                   point_distance_sq(0, 0, jx2, jy2) < point_distance_sq(0, 0, px, py):
                    blocked = True
                    break
        if not blocked:
            return True
    return False


def solve_one_case(mirrors):
    """處理一組測試資料，回傳每個鏡子的可見性（1=可見，0=不可見）"""
    result = []
    for i, (sx, sy, ex, ey) in enumerate(mirrors):
        visible = is_visible_from_origin(sx, sy, ex, ey, mirrors, i)
        result.append(1 if visible else 0)
    return result


def main():
    """主程式：從標準輸入讀取資料並輸出結果"""
    import sys
    data = sys.stdin.read().strip().splitlines()
    idx = 0
    out_lines = []
    while idx < len(data):
        line = data[idx].strip()
        if not line:
            idx += 1
            continue
        n = int(line)
        idx += 1
        mirrors = []
        for _ in range(n):
            sx, sy, ex, ey = map(int, data[idx].strip().split())
            mirrors.append((sx, sy, ex, ey))
            idx += 1
        result = solve_one_case(mirrors)
        out_lines.append(" ".join(map(str, result)))
    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
