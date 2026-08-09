#!/usr/bin/env python3
"""기여 통계를 수집해 하이스코어 보드 SVG를 만든다.

실패하면 0이 아닌 코드로 끝나고 기존 score.svg를 건드리지 않는다.
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contrib  # noqa: E402
import pixelfont as pf  # noqa: E402

USER, START_YEAR = "playok", 2010
W, H = 900, 460
BG, PANEL = "#0d0221", "#190b3d"
CYAN, MAGENTA, YELLOW, GREEN, TEXT, DIM = (
    "#00f0ff", "#ff2e88", "#ffd700", "#39ff14", "#e8e6f0", "#8b86a8")

CHART_X, CHART_Y, CHART_W, CHART_H = 44, 262, W - 88, 104


def comma(n):
    return f"{n:,}"


def build(stats):
    out = [pf.svg_header(W, H)]
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="{PANEL}" '
               f'stroke="{YELLOW}" stroke-width="4"/>')

    out.append(pf.text_rects("HIGH SCORE", 44, 44, 4, YELLOW))

    # NEW RECORD 배지: 올해가 역대 최고일 때만
    peak_year = max(stats["by_year"], key=lambda y: stats["by_year"][y])
    if peak_year == str(stats["year"]):
        badge = f'NEW RECORD {stats["year"]}'
        bw = pf.text_width(badge, 3)
        bx = W - 60 - bw
        out.append(f'<g><rect x="{bx - 12}" y="38" width="{bw + 24}" height="34" '
                   f'fill="{MAGENTA}"/>{pf.text_rects(badge, bx, 45, 3, BG)}'
                   f'<animate attributeName="opacity" values="1;1;0.25;1" '
                   f'dur="1.6s" repeatCount="indefinite"/></g>')

    total = comma(stats["total"])
    out.append(pf.text_rects(total, 44, 90, 9, YELLOW))
    out.append(pf.text_rects("TOTAL CONTRIBUTIONS SINCE 2010",
                             44 + pf.text_width(total, 9) + 28, 116, 3, DIM))

    # 요약 4칸
    cells = [
        ("MAX COMBO", f'{stats["max_combo"]} DAYS', GREEN),
        ("NOW", f'{stats["current_combo"]} DAYS', GREEN),
        ("BEST DAY", f'{stats["best_day"]} HITS', CYAN),
        (str(stats["year"]), f'{comma(stats["year_total"])} HITS', MAGENTA),
    ]
    cw = (W - 88) // 4
    for i, (label, value, color) in enumerate(cells):
        x = 44 + i * cw
        out.append(f'<rect x="{x}" y="172" width="{cw - 12}" height="66" '
                   f'fill="#000" opacity="0.35" stroke="{color}" stroke-width="2"/>')
        out.append(pf.text_rects(label, x + 14, 186, 2, DIM))
        out.append(pf.text_rects(value, x + 14, 208, 3, color))

    # 연도별 막대
    years = sorted(y for y in stats["by_year"] if int(y) >= 2015)
    peak = max(stats["by_year"][y] for y in years) or 1
    slot = CHART_W / len(years)
    bw = max(6, int(slot * 0.62))
    for i, y in enumerate(years):
        v = stats["by_year"][y]
        h = max(3, int(CHART_H * v / peak))
        x = int(CHART_X + i * slot + (slot - bw) / 2)
        color = MAGENTA if v == peak else CYAN
        out.append(f'<rect x="{x}" y="{CHART_Y + CHART_H - h}" width="{bw}" '
                   f'height="{h}" fill="{color}"/>')
        yw = pf.text_width(y[2:], 2)
        out.append(pf.text_rects(y[2:], int(x + (bw - yw) / 2),
                                 CHART_Y + CHART_H + 12, 2, DIM))
        vw = pf.text_width(str(v), 2)
        out.append(pf.text_rects(str(v), int(x + (bw - vw) / 2),
                                 CHART_Y + CHART_H + 32, 2, TEXT))

    out.append(f'<rect x="{CHART_X}" y="{CHART_Y + CHART_H}" width="{CHART_W}" '
               f'height="2" fill="{DIM}"/>')
    out.append(pf.text_rects(f'UPDATED {stats["updated"].replace("-", ".")}',
                             44, H - 38, 2, DIM))

    out.append(pf.scanlines(W, H))
    out.append(pf.svg_footer())
    return "".join(out)


def main():
    today = os.environ.get("PLAYOK_TODAY") or date.today().isoformat()
    days = contrib.collect(USER, START_YEAR, today)
    stats = contrib.summarize(days, today)
    if stats["total"] <= 0:
        raise ValueError(f"총 기여가 {stats['total']} — 수집이 잘못됐다")

    svg = build(stats)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "score.svg")
    with open(os.path.normpath(path), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote score.svg: total={stats['total']} year={stats['year_total']}")


if __name__ == "__main__":
    sys.exit(main() or 0)
