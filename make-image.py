#!/usr/bin/env python3
"""Draw 'The World in One Picture - 21 November 2026'.

One 1024x1024 PNG summing up Saturday 21 November 2026's world news:
six verified stories, each with a drawn icon, a headline and two lines
of text. Deterministic: no randomness, no network, no timestamps.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 241, 227)      # warm paper
CARD = (255, 253, 246)       # panel card
INK = (26, 42, 74)           # dark navy ink
TEAL = (15, 118, 110)
AMBER = (180, 83, 9)
RED = (185, 28, 28)
GREEN = (21, 101, 52)
GREY = (90, 96, 110)
RULE = (26, 42, 74)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


TITLE_F = font("DejaVuSerif-Bold.ttf", 46)
DATE_F = font("DejaVuSans-Bold.ttf", 20)
KICK_F = font("DejaVuSans-Bold.ttf", 13)
HEAD_F = font("DejaVuSerif-Bold.ttf", 21)
BODY_F = font("DejaVuSans.ttf", 15)
FACT_F = font("DejaVuSans-Bold.ttf", 13)
FOOT_F = font("DejaVuSans.ttf", 12)


def wrap(text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if fnt.getlength(trial) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_icon(d, kind, x, y, s, accent):
    """Small drawn illustration, s x s box at (x, y)."""
    if kind == "missile":
        # clean diagonal rocket: dark body, red nose, amber flame,
        # two grey motion lines trailing behind it
        d.line([(x + 14, y + 50), (x + 46, y + 18)], fill=INK, width=10)
        d.polygon([(x + 46, y + 18), (x + 60, y + 12), (x + 54, y + 28)],
                  fill=RED)
        d.polygon([(x + 14, y + 50), (x + 4, y + 54), (x + 14, y + 60)],
                  fill=INK)
        d.polygon([(x + 14, y + 50), (x + 20, y + 60), (x + 10, y + 60)],
                  fill=INK)
        d.polygon([(x + 12, y + 52), (x + 2, y + 58), (x + 8, y + 62)],
                  fill=AMBER)
        d.line([(x + 10, y + 32), (x + 22, y + 20)], fill=GREY, width=2)
        d.line([(x + 20, y + 44), (x + 32, y + 32)], fill=GREY, width=2)
    elif kind == "market":
        # falling bars + red down arrow
        bars = [(0, 30), (16, 42), (32, 54)]
        for i, (bx, bh) in enumerate(bars):
            d.rectangle([x + bx, y + 58 - bh, x + bx + 12, y + 58],
                        fill=TEAL if i < 2 else RED)
        d.line([(x + 2, y + 6), (x + 22, y + 24), (x + 38, y + 20),
                (x + 58, y + 44)], fill=RED, width=4)
        d.polygon([(x + 58, y + 44), (x + 48, y + 42), (x + 56, y + 54)],
                  fill=RED)
    elif kind == "climate":
        # globe with equator and meridian, plus a small clock badge
        d.ellipse([x + 4, y + 4, x + s - 16, y + s - 16], outline=TEAL, width=3)
        d.ellipse([x + 4, y + 4, x + s - 16, y + s - 16], fill=(223, 240, 236))
        d.arc([x + 12, y + 8, x + s - 24, y + s - 24], start=90, end=270,
              fill=TEAL, width=2)
        d.line([(x + s // 2 - 6, y + 8), (x + s // 2 - 6, y + s - 20)],
               fill=TEAL, width=2)
        d.line([(x + 8, y + s // 2 - 6), (x + s - 20, y + s // 2 - 6)],
               fill=TEAL, width=2)
        d.ellipse([x + s - 26, y + s - 26, x + s - 2, y + s - 2],
                  fill=CARD, outline=AMBER, width=3)
        d.line([(x + s - 14, y + s - 14), (x + s - 14, y + s - 22)],
               fill=AMBER, width=2)
        d.line([(x + s - 14, y + s - 14), (x + s - 8, y + s - 12)],
               fill=AMBER, width=2)
    elif kind == "quake":
        # mountains with a seismic zigzag
        d.polygon([(x + 2, y + s - 6), (x + 22, y + 18), (x + 42, y + s - 6)],
                  fill=INK)
        d.polygon([(x + 24, y + s - 6), (x + 44, y + 26), (x + 62, y + s - 6)],
                  fill=(70, 84, 110))
        d.polygon([(x + 18, y + 22), (x + 22, y + 18), (x + 26, y + 22),
                   (x + 22, y + 26)], fill=(255, 255, 255))
        pts = [(x + 2, y + 34), (x + 12, y + 28), (x + 18, y + 40),
               (x + 26, y + 26), (x + 34, y + 38), (x + 42, y + 30),
               (x + 50, y + 40), (x + 60, y + 32)]
        d.line(pts, fill=RED, width=3)
    elif kind == "jail":
        # barred building with a 2032 tag
        d.rectangle([x + 8, y + 6, x + s - 8, y + s - 6], outline=INK, width=3)
        d.rectangle([x + 8, y + 6, x + s - 8, y + 20], fill=INK)
        for bx in (16, 26, 36, 46):
            d.line([(x + bx, y + 22), (x + bx, y + s - 8)], fill=INK, width=3)
        d.rectangle([x + s - 30, y + s - 22, x + s - 2, y + s - 6],
                    fill=AMBER)
        d.text((x + s - 27, y + s - 20), "32", font=font("DejaVuSans-Bold.ttf", 11),
               fill=(255, 255, 255))
    elif kind == "india":
        # rising chart with coins
        pts = [(x + 4, y + 46), (x + 18, y + 38), (x + 30, y + 42),
               (x + 46, y + 24), (x + 60, y + 10)]
        d.line(pts, fill=GREEN, width=4)
        d.polygon([(x + 60, y + 10), (x + 50, y + 10), (x + 58, y + 20)],
                  fill=GREEN)
        d.ellipse([x + 6, y + 50, x + 20, y + 62], fill=AMBER,
                  outline=(146, 64, 14), width=1)
        d.ellipse([x + 24, y + 52, x + 38, y + 64], fill=AMBER,
                  outline=(146, 64, 14), width=1)


STORIES = [
    dict(kind="missile", accent=RED, kicker="POLAND  ·  CONFLICT",
         head="A Russian missile lands in Poland",
         body=("A Kh-101 cruise missile came down in south-east Poland "
               "during a huge air attack on Ukraine. No one was hurt; "
               "NATO jets scrambled."),
         fact="Warsaw calls it a deliberate provocation"),
    dict(kind="market", accent=RED, kicker="MARKETS  ·  ECONOMY",
         head="Wall Street slides into correction",
         body=("AI shares led a sharp sell-off: the S&P 500 fell 3.7% "
               "and the Nasdaq 5.3%, pushing the S&P and the Dow into "
               "correction territory."),
         fact="Nvidia -13.8% as the SEC checks its accounts"),
    dict(kind="climate", accent=TEAL, kicker="CLIMATE  ·  ANTALYA",
         head="COP31 runs into overtime",
         body=("Climate talks in Antalya missed their Friday deadline. "
               "The draft deal drops every mention of fossil fuels; "
               "island nations warn of failure."),
         fact="Draft cut from 144 paragraphs to 80"),
    dict(kind="quake", accent=AMBER, kicker="PERU  ·  DISASTER",
         head="Magnitude 6.8 quake shakes the Andes",
         body=("A deep quake struck the Junín region of central Peru and "
               "was felt in Lima, 320 km away. No casualties or major "
               "damage were reported."),
         fact="Depth 129 km · felt across the capital"),
    dict(kind="jail", accent=INK, kicker="NEW YORK  ·  POLITICS",
         head="Rikers Island to close by 2032",
         body=("Mayor Zohran Mamdani unveiled a plan to shut New York's "
               "notorious jail complex and replace it with four smaller "
               "borough jails."),
         fact="Inmates to fall from 6,500 to 4,100"),
    dict(kind="india", accent=GREEN, kicker="INDIA  ·  ECONOMY",
         head="Record rush into Indian shares",
         body=("Foreign investors put a net Rs 1.22 lakh crore into "
               "Indian equities in November — the biggest monthly "
               "inflow on record."),
         fact="Beats the 2020 record of Rs 70,896 crore"),
]


def draw_panel(d, story, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=(200, 190, 168),
                width=1)
    d.rectangle([x, y, x + w, y + 5], fill=story["accent"])
    px, py = x + 14, y + 18
    draw_icon(d, story["kind"], px, py, 64, story["accent"])
    tx = x + 92
    d.text((tx, y + 18), story["kicker"], font=KICK_F, fill=TEAL)
    head_lines = wrap(story["head"], HEAD_F, w - 92 - 14)
    hy = y + 40
    for ln in head_lines[:2]:
        d.text((tx, hy), ln, font=HEAD_F, fill=INK)
        hy += 26
    body_lines = wrap(story["body"], BODY_F, w - 28)
    by = y + 106
    for ln in body_lines[:3]:
        d.text((x + 14, by), ln, font=BODY_F, fill=(38, 48, 66))
        by += 20
    fy = y + h - 34
    d.line([(x + 14, fy - 8), (x + w - 14, fy - 8)], fill=(210, 200, 178),
           width=1)
    fact_lines = wrap(story["fact"], FACT_F, w - 28)
    d.text((x + 14, fy), fact_lines[0], font=FACT_F, fill=story["accent"])


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 118], fill=INK)
    title = "THE WORLD IN ONE PICTURE"
    tw = d.textlength(title, font=TITLE_F)
    d.text(((W - tw) / 2, 16), title, font=TITLE_F, fill=(247, 241, 227))
    date = "SATURDAY  ·  21 NOVEMBER 2026"
    dw = d.textlength(date, font=DATE_F)
    d.text(((W - dw) / 2, 74), date, font=DATE_F, fill=(232, 180, 90))
    d.rectangle([0, 118, W, 121], fill=AMBER)

    # six panels: 2 columns x 3 rows
    mx, my = 28, 136
    pw = (W - 2 * mx - 20) // 2
    ph = 270
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = mx + col * (pw + 20)
        y = my + row * (ph + 16)
        draw_panel(d, story, x, y, pw, ph)

    # footer
    foot = ("Drawn from live reporting  ·  Reuters  ·  AP  ·  BBC  ·  CNBC  —  "
            "21 November 2026")
    fw = d.textlength(foot, font=FOOT_F)
    d.text(((W - fw) / 2, 990), foot, font=FOOT_F, fill=GREY)

    img.save("entry.png", "PNG")


if __name__ == "__main__":
    main()
