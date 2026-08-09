#!/usr/bin/env python3
"""프로필 상단 타이틀 배너 SVG를 만든다."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pixelfont as pf  # noqa: E402

W, H = 900, 280
BG = "#0d0221"
CYAN, MAGENTA, YELLOW, DIM = "#00f0ff", "#ff2e88", "#ffd700", "#8b86a8"

STARS = [(60, 40), (150, 90), (240, 35), (330, 120), (420, 60),
         (510, 100), (600, 45), (690, 130), (780, 70), (850, 110),
         (110, 190), (300, 215), (520, 200), (740, 225), (830, 185)]


def main():
    out = [pf.svg_header(W, H)]
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    for i, (x, y) in enumerate(STARS):
        c = [CYAN, MAGENTA, "#ffffff"][i % 3]
        out.append(f'<rect x="{x}" y="{y}" width="2" height="2" fill="{c}" opacity="0.8"/>')

    # 로고: PLAYOK, px=10 -> 폭 = 6*5*10 + 5*10 = 350
    logo = "PLAYOK"
    px = 10
    lw = pf.text_width(logo, px)
    lx, ly = (W - lw) // 2, 62
    out.append(pf.text_rects(logo, lx + 5, ly + 5, px, MAGENTA))  # 그림자
    out.append(pf.text_rects(logo, lx, ly, px, CYAN))

    sub = "SYSTEMS ENGINEER  SEOUL  SINCE 2010"
    sw = pf.text_width(sub, 3)
    out.append(pf.text_rects(sub, (W - sw) // 2, 160, 3, DIM))

    # PRESS START: 1.2초 주기 깜빡임
    ps = "PRESS START"
    pw = pf.text_width(ps, 4)
    out.append(f'<g>{pf.text_rects(ps, (W - pw) // 2, 210, 4, YELLOW)}'
               f'<animate attributeName="opacity" values="1;1;0;0;1" '
               f'dur="1.2s" repeatCount="indefinite"/></g>')

    out.append(pf.scanlines(W, H))
    out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" '
               f'stroke="{CYAN}" stroke-width="6"/>')
    out.append(pf.svg_footer())

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "title.svg")
    with open(os.path.normpath(path), "w", encoding="utf-8") as f:
        f.write("".join(out))
    print("wrote title.svg")


if __name__ == "__main__":
    main()
