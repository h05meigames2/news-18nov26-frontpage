#!/usr/bin/env python3
"""Render the front page for 18 November 2026 world news.

Draws a single 1024x1024 newspaper front page with PIL: a masthead
naming the day, then six drawn panels, each with a procedural pictogram
and a short factual headline. Run: python3 gen_image.py
Writes entry.png next to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 240, 220)
INK = (20, 38, 74)
RED = (179, 38, 30)
BLUE = (38, 84, 138)
GOLD = (198, 142, 32)
TEAL = (18, 110, 105)
GREY = (90, 92, 96)
LIGHT = (255, 252, 240)
RULE = (20, 38, 74)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 60)
F_DATE = font("DejaVuSans-Bold.ttf", 34)
F_KICK = font("DejaVuSans-Bold.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_HEAD_SM = font("DejaVuSans-Bold.ttf", 24)
F_HEAD_XS = font("DejaVuSans-Bold.ttf", 22)
F_BODY = font("DejaVuSans.ttf", 19)
F_BODY_SM = font("DejaVuSans.ttf", 17)
F_TICK = font("DejaVuSans-Bold.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def headline(draw, x, y, w, text, fnt=F_HEAD, color=INK, gap=4):
    lines = wrap(draw, text, fnt, w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += fnt.size + gap
    return y


def panel(draw, x, y, w, h, kicker, kcolor=RED):
    draw.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=INK, width=3)
    draw.rectangle([x, y, x + w, y + 34], fill=INK)
    draw.text((x + 12, y + 6), kicker, font=F_KICK, fill=(255, 255, 255))
    return y + 44


def radar_pic(draw, cx, cy, s):
    # radar dish sweeping over a sea line, with a drone above
    draw.arc([cx - s, cy - s, cx + s, cy + s], 200, 340, fill=BLUE, width=6)
    draw.line([cx, cy, cx - s * 0.8, cy + s * 0.55], fill=BLUE, width=6)
    draw.line([cx, cy, cx + s * 0.7, cy - s * 0.6], fill=TEAL, width=5)
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)
    for r in (s * 0.45, s * 0.75):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=BLUE, width=3)
    # drone
    dx, dy = cx + s * 0.95, cy - s * 0.85
    draw.ellipse([dx - 26, dy - 8, dx + 26, dy + 8], fill=INK)
    draw.ellipse([dx - 34, dy - 12, dx - 14, dy - 4], outline=INK, width=3)
    draw.ellipse([dx + 14, dy - 12, dx + 34, dy - 4], outline=INK, width=3)


def tanker_pic(draw, x, y, w, h):
    # tanker hull on waves with a flame plume
    draw.rectangle([x, y + h * 0.45, x + w, y + h * 0.72], fill=RED)
    draw.rectangle([x + w * 0.08, y + h * 0.72, x + w * 0.92, y + h * 0.82],
                   fill=INK)
    draw.rectangle([x + w * 0.62, y + h * 0.12, x + w * 0.82, y + h * 0.45],
                   fill=LIGHT, outline=INK, width=3)
    for i in range(3):
        draw.rectangle([x + w * 0.10 + i * w * 0.16, y + h * 0.30,
                        x + w * 0.22 + i * w * 0.16, y + h * 0.45],
                       fill=BLUE, outline=INK, width=2)
    # flame
    fx = x + w * 0.72
    draw.polygon([(fx - 26, y + h * 0.16), (fx, y - 6), (fx + 26, y + h * 0.16),
                  (fx + 12, y + h * 0.10), (fx, y + h * 0.22),
                  (fx - 12, y + h * 0.10)], fill=GOLD, outline=RED)
    for i in range(3):
        wx = x + i * w * 0.36
        draw.arc([wx, y + h * 0.86, wx + w * 0.30, y + h * 1.02],
                 180, 360, fill=BLUE, width=4)


def flags_pic(draw, x, y, w, h):
    # four small Quad flags on poles: US, India, Japan, Australia
    cols = [(RED, (255, 255, 255), BLUE), (GOLD, (255, 255, 255), TEAL),
            ((255, 255, 255), RED, (255, 255, 255)),
            (BLUE, RED, (255, 255, 255))]
    fw, fh = w // 4 - 10, h * 0.55
    for i, (c1, c2, c3) in enumerate(cols):
        fx = x + i * (fw + 10)
        draw.line([fx + fw // 2, y + fh, fx + fw // 2, y + h], fill=INK, width=4)
        draw.rectangle([fx, y, fx + fw, y + fh / 3], fill=c1)
        draw.rectangle([fx, y + fh / 3, fx + fw, y + 2 * fh / 3], fill=c2)
        draw.rectangle([fx, y + 2 * fh / 3, fx + fw, y + fh], fill=c3)
        if i == 2:
            draw.ellipse([fx + fw // 2 - 9, y + fh // 2 - 9,
                          fx + fw // 2 + 9, y + fh // 2 + 9], fill=RED)


def cyclone_pic(draw, cx, cy, r):
    for i, rr in enumerate(range(r, 8, -14)):
        start = 20 + i * 55
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], start, start + 250,
                 fill=TEAL if i % 2 == 0 else BLUE, width=7)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=RED)
    draw.polygon([(cx - 60, cy + r + 4), (cx + 60, cy + r + 4),
                  (cx + 34, cy + r + 26), (cx - 34, cy + r + 26)],
                 fill=GOLD)


def trophy_pic(draw, cx, cy, s):
    draw.polygon([(cx - s, cy - s), (cx + s, cy - s), (cx + s * 0.55, cy),
                  (cx + s * 0.3, cy + s * 0.5), (cx + s * 0.55, cy + s * 0.85),
                  (cx - s * 0.55, cy + s * 0.85), (cx - s * 0.3, cy + s * 0.5),
                  (cx - s * 0.55, cy)], fill=GOLD, outline=INK, width=3)
    draw.arc([cx - s * 1.35, cy - s * 0.9, cx - s * 0.4, cy + s * 0.1],
             90, 270, fill=GOLD, width=8)
    draw.arc([cx + s * 0.4, cy - s * 0.9, cx + s * 1.35, cy + s * 0.1],
             270, 90, fill=GOLD, width=8)
    draw.text((cx - 8, cy - s * 0.72), "1", font=font("DejaVuSans-Bold.ttf", 34),
              fill=INK)


def chip_pic(draw, cx, cy, s):
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], fill=INK)
    draw.rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55],
                   fill=TEAL, outline=GOLD, width=3)
    draw.text((cx - 14, cy - 16), "AI", font=font("DejaVuSans-Bold.ttf", 30),
              fill=(255, 255, 255))
    for i in range(4):
        off = -s * 0.6 + i * s * 0.4
        draw.line([cx + off, cy - s, cx + off, cy - s - 16], fill=INK, width=5)
        draw.line([cx + off, cy + s, cx + off, cy + s + 16], fill=INK, width=5)
        draw.line([cx - s, cy + off, cx - s - 16, cy + off], fill=INK, width=5)
        draw.line([cx + s, cy + off, cx + s + 16, cy + off], fill=INK, width=5)
    # warning triangle
    tx, ty = cx + s + 34, cy - s - 10
    draw.polygon([(tx, ty - 22), (tx + 22, ty + 14), (tx - 22, ty + 14)],
                 fill=GOLD, outline=RED, width=3)
    draw.text((tx - 4, ty - 12), "!", font=font("DejaVuSans-Bold.ttf", 24),
              fill=RED)


def parliament_pic(draw, x, y, w, h):
    # simple parliament building with columns and a gavel
    draw.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.92, y + h * 0.88],
                   fill=LIGHT, outline=INK, width=3)
    draw.polygon([(x + w * 0.02, y + h * 0.44), (x + w * 0.5, y + h * 0.06),
                  (x + w * 0.98, y + h * 0.44)], fill=BLUE, outline=INK, width=3)
    for i in range(4):
        cx = x + w * (0.20 + i * 0.20)
        draw.rectangle([cx - 9, y + h * 0.50, cx + 9, y + h * 0.86], fill=INK)
    draw.rectangle([x + w * 0.72, y + h * 0.55, x + w * 0.98, y + h * 0.66],
                   fill=GOLD, outline=INK, width=2)
    draw.line([x + w * 0.80, y + h * 0.55, x + w * 0.92, y + h * 0.30],
              fill=INK, width=5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=4)

    # ---- masthead ----
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 34), title, font=F_TITLE, fill=INK)
    d.line([40, 128, W - 40, 128], fill=INK, width=3)
    d.rectangle([40, 138, W - 40, 182], fill=RED)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 144), date, font=F_DATE, fill=(255, 255, 255))
    sub = "ONE DAY  •  SIX STORIES  •  AROUND THE GLOBE"
    sw = d.textlength(sub, font=F_KICK)
    d.text(((W - sw) / 2, 192), sub, font=F_KICK, fill=GREY)

    # ---- hero: Hormuz / Iran-US (left, wide) ----
    hx, hy, hw, hh = 28, 224, 596, 330
    y = panel(d, hx, hy, hw, hh, "MIDDLE EAST — WAR AT SEA")
    radar_pic(d, hx + 130, hy + 150, 78)
    tanker_pic(d, hx + 300, hy + 108, 260, 130)
    y = headline(d, hx + 16, hy + 238, hw - 32,
                 "IRAN HITS US RADAR IN BAHRAIN — US STRIKES QESHM")
    d.text((hx + 16, y + 2),
           "Tanker hit in Hormuz; 21 of 24 Indian crew evacuated.",
           font=F_BODY, fill=GREY)

    # ---- right column top: Quad / Manila ----
    rx, rw = 640, 356
    y = panel(d, rx, 224, rw, 184, "ASIA — QUAD TALKS")
    flags_pic(d, rx + 18, 272, rw - 36, 56)
    headline(d, rx + 16, 348, rw - 32, "TRUMP IN MANILA BEFORE CHINA TRIP",
             fnt=F_HEAD_SM)

    # ---- right column bottom: cyclone ----
    y = panel(d, rx, 416, rw, 138, "WEATHER — BAY OF BENGAL")
    cyclone_pic(d, rx + 58, 492, 36)
    headline(d, rx + 124, 462, rw - 140, "CYCLONE AKVAN BEARS DOWN ON INDIA",
             fnt=F_HEAD_XS)

    # ---- bottom row: three panels ----
    by, bh = 570, 306
    bw = 312
    xs = [28, 356, 684]

    y = panel(d, xs[0], by, bw, bh, "SPORT — DHAKA")
    trophy_pic(d, xs[0] + bw // 2, by + 112, 48)
    y = headline(d, xs[0] + 14, by + 188, bw - 28,
                 "INDIA LIFTS 10TH SAFF TITLE", fnt=F_HEAD_XS)
    d.text((xs[0] + 14, y + 2), "Beats Pakistan 2–1 in the final.",
           font=F_BODY_SM, fill=GREY)

    y = panel(d, xs[1], by, bw, bh, "TECH — AI BUBBLE?")
    chip_pic(d, xs[1] + bw // 2 - 14, by + 116, 48)
    y = headline(d, xs[1] + 14, by + 188, bw - 28,
                 "BAIDU CHIEF WARNS OF AI BUBBLE", fnt=F_HEAD_XS)
    d.text((xs[1] + 14, y + 2), "Warning ahead of APEC talks.",
           font=F_BODY_SM, fill=GREY)

    y = panel(d, xs[2], by, bw, bh, "POLITICS")
    parliament_pic(d, xs[2] + 24, by + 56, bw - 48, 116)
    y = headline(d, xs[2] + 14, by + 188, bw - 28,
                 "UK SANCTIONS SETTLER FIRMS", fnt=F_HEAD_XS)
    for line in wrap(d, "Israel picks Eisenkot as speaker.",
                     F_BODY_SM, bw - 28):
        d.text((xs[2] + 14, y + 2), line, font=F_BODY_SM, fill=GREY)
        y += F_BODY_SM.size + 3

    # ---- ticker strip ----
    d.rectangle([28, 892, W - 28, 946], fill=INK)
    d.text((44, 908),
           "ALSO: Vance — Iran must cut enrichment  •  US security net reported down",
           font=F_TICK, fill=(255, 255, 255))
    d.text((28, 962),
           "Front page drawn from reports of Wednesday 18 November 2026  •  All stories as reported that day.",
           font=F_FOOT, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
