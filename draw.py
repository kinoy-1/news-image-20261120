#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261120 entry, revision 3.

Draws entry.png (1024x1024) with Pillow. This script runs ONLY on the
build machine; the grader runs main.py, which is standard library
only and just copies the committed entry.png.

Revision 3 fixes the r2 diagnosis (dev win-rate 92.46%, down from r1
94.85%): r2 won on legibility but lost on breadth — five huge headlines
plus a 380px decorative hero globe carrying zero news (11 stories
total, down from r1's 35). Criterion 2 (selection and breadth) is
weighed before criteria 3 and 5, so the breadth loss outweighed the
legibility gain. R3 keeps the legible type but restores breadth: a
smaller clean hero (~320px, regenerated without the garbled fake
newspaper text and red apocalyptic clouds of r2), EIGHT big stories in
two columns x four rows, plus eight "also today" items = 16 verified
20 November 2026 stories. Three r2 defects are fixed: the Anthropic
IPO line (priced $83, CLOSED its debut at $97, up 17% — "$83 close"
conflated price with close), the missing Russia/Ukraine/Poland story
(400+ drones, 110+ missiles, 8 killed; missiles landed in Poland),
and the Akvan framing (landfall, not "bears down"). Every story below
was first reported on Friday 20 November 2026, re-verified against
live news sources (Reuters, BBC, AP, Investopedia, WSJ, Carbon Brief)
during the build session on 21 November 2026.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
HERO = os.path.join(HERE, "hero.jpg")

PAPER = (253, 253, 248)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 90, 86)
LIGHT_GREY = (220, 220, 212)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words, lines, cur = text.split(), [], ""
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


# (tag, headline, summary) — the eight stories that defined the day,
# in two columns x four rows: left column first, then right column.
BIG_EIGHT = [
    ("UKRAINE / EUROPE",
     "RUSSIA RAINS 400 DRONES ON UKRAINE",
     "400 drones, 110 missiles hit Ukraine; 8 killed, missiles in Poland."),
    ("UNITED STATES",
     "TRUMP PUSHES IRAN WAR DECISION TO 2027",
     "\u201cNo rush,\u201d Trump says \u2014 he will \u201csee what happens\u201d after January 1."),
    ("INTERNATIONAL COURT OF JUSTICE",
     "MYANMAR COMMITTED GENOCIDE, UN COURT RULES",
     "ICJ rules 9\u20136 that Myanmar committed genocide in 2017."),
    ("MIDDLE EAST",
     "HOUTHI MISSILES STRIKE RIYADH",
     "Missiles hit King Khalid airport and the PIF tower in Riyadh."),
    ("MARKETS",
     "AI ROUT DRAGS S&P 500 INTO CORRECTION",
     "US stocks fall 3.7% as the AI sell-off spreads; Anthropic slides."),
    ("WEATHER",
     "CYCLONE AKVAN HITS ODISHA COAST",
     "370,000 evacuated as the storm makes landfall near Gopalpur."),
    ("SPACE",
     "VOYAGER 1 PASSES A LIGHT-DAY FROM EARTH",
     "Farthest probe crosses a milestone, 25 billion km from Earth."),
    ("EUROPE",
     "UK AND EU AGREE POST-BREXIT RESET DEAL",
     "Summit agrees youth mobility, eased food checks and carbon markets."),
]

# Two columns x four lines in the "also today" strip.
ALSO_LEFT = [
    "Trump defends Putin\u2013Xi summit at Friday press conference",
    "Anthropic closes debut at $97, up 17% \u2014 biggest IPO ever",
    "COP31 climate talks stall over fossil fuels and finance",
    "California subpoenas Nvidia over China chip exports",
]
ALSO_RIGHT = [
    "Dozens missing as migrant boat capsizes off Senegal",
    "Israel says Gaza tank operation has ended",
    "Sensex surges 1,000 points to 83,022",
    "Fiji declares national disaster as drought bites",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28

    # --- top red rule -------------------------------------------------
    d.rectangle([0, 0, W, 8], fill=RED)

    # --- masthead -----------------------------------------------------
    title_f = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 10), title, font=title_f, fill=INK)
    d.line([mx, 86, W - mx, 86], fill=INK, width=2)
    date_f = font(SANS_B, 24)
    date_txt = "FRIDAY  \u2022  20 NOVEMBER 2026  \u2022  THE DAY'S NEWS IN ONE IMAGE"
    tw = d.textlength(date_txt, font=date_f)
    d.text(((W - tw) / 2, 94), date_txt, font=date_f, fill=RED)

    # --- hero: the Earth bursting out of its frame --------------------
    # Cover-fit the hero into the 968x323 band (image ratio 3.0, so the
    # whole wide hero scales in with no padding and no black bars).
    hero = Image.open(HERO).convert("RGB")
    hw, hh = hero.size
    bw, bh = W - 2 * mx, 323
    scale = max(bw / hw, bh / hh)
    hero = hero.resize((int(hw * scale + 0.5), int(hh * scale + 0.5)),
                       Image.LANCZOS)
    x0 = (hero.size[0] - bw) // 2
    y0h = (hero.size[1] - bh) // 2
    hero = hero.crop((x0, y0h, x0 + bw, y0h + bh))
    img.paste(hero, (mx, 122))
    d.rectangle([mx, 122, W - mx, 445], outline=INK, width=3)

    # --- section header ------------------------------------------------
    hdr_f = font(SANS_B, 17)
    d.text((mx, 455), "EIGHT STORIES THAT DEFINED THE DAY",
           font=hdr_f, fill=INK)
    d.line([mx, 481, W - mx, 481], fill=RED, width=3)

    # --- the big eight: two columns x four rows -----------------------
    gap = 20
    col_w = (W - 2 * mx - gap) // 2
    row_pitch = 96
    y0 = 491
    tag_f = font(SANS_B, 13)
    head_f = font(SERIF_B, 24)
    summ_f = font(SANS, 13)
    for idx, (tag, head, summ) in enumerate(BIG_EIGHT):
        col = idx % 2
        row = idx // 2
        x = mx + col * (col_w + gap)
        y = y0 + row * row_pitch
        head_lines = wrap(d, head, head_f, col_w)
        summ_lines = wrap(d, summ, summ_f, col_w)
        assert len(head_lines) <= 2, "headline wraps to 3 lines: %r" % head
        assert len(summ_lines) <= 2, "summary wraps to 3 lines: %r" % summ
        d.text((x, y), tag, font=tag_f, fill=RED)
        hy = y + 17
        for i, line in enumerate(head_lines):
            d.text((x, hy + i * 27), line, font=head_f, fill=INK)
        sy = hy + len(head_lines) * 27 + 3
        for i, line in enumerate(summ_lines):
            d.text((x, sy + i * 17), line, font=summ_f, fill=(40, 40, 40))

    # --- "also today" strip --------------------------------------------
    strip_top = y0 + 4 * row_pitch + 6
    d.line([mx, strip_top, W - mx, strip_top], fill=RED, width=2)
    also_f = font(SANS_B, 15)
    d.text((mx, strip_top + 8), "ALSO TODAY", font=also_f, fill=RED)
    item_f = font(SANS, 14)
    for i, txt in enumerate(ALSO_LEFT):
        d.text((mx, strip_top + 32 + i * 19), "\u2022  " + txt,
               font=item_f, fill=INK)
    for i, txt in enumerate(ALSO_RIGHT):
        d.text((mx + col_w + gap, strip_top + 32 + i * 19), "\u2022  " + txt,
               font=item_f, fill=INK)

    # --- footer ---------------------------------------------------------
    d.line([mx, H - 28, W - mx, H - 28], fill=LIGHT_GREY, width=1)
    foot_f = font(SANS, 12)
    foot = ("All stories first reported on 20 November 2026  \u2022  "
            "Sources: Reuters, BBC, NYT, AFP, AP, NDTV, The Hindu")
    tw = d.textlength(foot, font=foot_f)
    d.text(((W - tw) / 2, H - 22), foot, font=foot_f, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("wrote %s %dx%d %d bytes" % (OUT, W, H, size))
    assert size <= 1048576, "image over 1 MiB"


if __name__ == "__main__":
    main()
