#!/usr/bin/env python3
"""플레이어 스탯 카드 SVG를 만든다.

EXP 게이지 값은 공개 저장소의 주 언어 개수다. 자주 바뀌지 않으므로 상수로 둔다.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pixelfont as pf  # noqa: E402

W, H = 900, 340
BG, PANEL = "#0d0221", "#190b3d"
CYAN, MAGENTA, YELLOW, GREEN, TEXT, DIM = (
    "#00f0ff", "#ff2e88", "#ffd700", "#39ff14", "#e8e6f0", "#8b86a8")

INFO = [
    ("CLASS", "SYSTEMS ENGINEER"),
    ("GUILD", "PENTASYSTEM INC."),
    ("LOC", "SEOUL, KR"),
    ("SINCE", "2010"),
]

LANGS = [("GO", 4, CYAN), ("RUST", 3, MAGENTA), ("HTML", 3, YELLOW),
         ("JS", 3, GREEN), ("C", 1, TEXT)]
MAX_LANG = 4


def main():
    out = [pf.svg_header(W, H)]
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="{PANEL}" '
               f'stroke="{CYAN}" stroke-width="4"/>')

    out.append(pf.text_rects("PLAYER STATS", 44, 44, 4, YELLOW))

    y = 110
    for label, value in INFO:
        out.append(pf.text_rects(label, 44, y, 3, MAGENTA))
        out.append(pf.text_rects(value, 190, y, 3, TEXT))
        y += 38

    # EXP 게이지
    gx, gy = 520, 110
    out.append(pf.text_rects("EXP", gx, 44, 4, DIM))
    for name, count, color in LANGS:
        out.append(pf.text_rects(name, gx, gy + 3, 3, DIM))
        bar_x = gx + 100
        segs = 18
        seg_w = 14
        for i in range(segs):
            lit = i < round(segs * count / MAX_LANG)
            fill = color if lit else "#000"
            op = "" if lit else ' opacity="0.45"'
            out.append(f'<rect x="{bar_x + i * seg_w}" y="{gy}" width="{seg_w - 2}" '
                       f'height="18" fill="{fill}"{op}/>')
        gy += 38

    out.append(pf.scanlines(W, H))
    out.append(pf.svg_footer())

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "stats.svg")
    with open(os.path.normpath(path), "w", encoding="utf-8") as f:
        f.write("".join(out))
    print("wrote stats.svg")


if __name__ == "__main__":
    main()
