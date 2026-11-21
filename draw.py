#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261120 entry, revision 2.

Draws entry.png (1024x1024) with Pillow. This script runs ONLY on the
build machine; the grader runs main.py, which is standard library
only and just copies the committed entry.png.

Revision 2 fixes the v1 diagnosis: v1 was a dense wall of 10-13pt text
in a 3x10 grid, unreadable at thumbnail size, with no dominant visual
(dev win-rate 94.85%). V2 is one giant picture plus five huge headlines
a picture editor can read in two seconds at thumbnail size: the Earth
bursting out of a torn newspaper frame (hero.jpg, generated for this
revision), then the day's five biggest stories in full-width rows, then
an "also today" strip. Every story below was first reported on Friday
20 November 2026 (or happened that day), verified against live news
sources during the build session.
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


# (tag, headline, summary) — the five stories that defined the day.
BIG_FIVE = [
    ("UNITED STATES",
     "TRUMP PUSHES IRAN WAR DECISION TO 2027",
     "\u201cNo rush,\u201d Trump says \u2014 he will \u201csee what happens\u201d after January 1."),
    ("INTERNATIONAL COURT OF JUSTICE",
     "MYANMAR COMMITTED GENOCIDE, UN COURT RULES",
     "The ICJ rules 9\u20136 that Myanmar committed genocide against the Rohingya in 2017."),
    ("MIDDLE EAST",
     "HOUTHI MISSILES STRIKE RIYADH",
     "Missiles hit King Khalid airport and the PIF tower in the Saudi capital."),
    ("WEATHER",
     "CYCLONE AKVAN BEARS DOWN ON ODISHA",
     "The cyclone churns toward India's east coast as evacuations begin."),
    ("SPACE",
     "VOYAGER 1 PASSES A LIGHT-DAY FROM EARTH",
     "Humanity's farthest probe crosses a new milestone, 25 billion km out."),
]

# Two columns x three lines in the "also today" strip.
ALSO_LEFT = [
    "Three nuclear powers, one table \u2014 Trump, Xi and Putin meet",
    "Jeffries set to be first Black Speaker of the House",
    "GTA VI sales pass $1.8 billion in days",
]
ALSO_RIGHT = [
    "Anthropic IPO closes today at $83 a share",
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
    d.text(((W - tw) / 2, 14), title, font=title_f, fill=INK)
    d.line([mx, 92, W - mx, 92], fill=INK, width=2)
    date_f = font(SANS_B, 24)
    date_txt = "FRIDAY  \u2022  20 NOVEMBER 2026  \u2022  THE DAY'S NEWS IN ONE IMAGE"
    tw = d.textlength(date_txt, font=date_f)
    d.text(((W - tw) / 2, 100), date_txt, font=date_f, fill=RED)

    # --- hero: the Earth bursting out of its frame --------------------
    hero = Image.open(HERO).convert("RGB")
    # Crop the wide hero to the 1024x380 band, keeping the globe centred.
    hw, hh = hero.size
    target_ratio = (W - 2 * mx) / 380.0
    crop_w = int(hh * target_ratio)
    x0 = (hw - crop_w) // 2
    hero = hero.crop((x0, 0, x0 + crop_w, hh))
    hero = hero.resize((W - 2 * mx, 380), Image.LANCZOS)
    img.paste(hero, (mx, 130))
    d.rectangle([mx, 130, W - mx, 510], outline=INK, width=3)

    # --- section header ------------------------------------------------
    hdr_f = font(SANS_B, 17)
    d.text((mx, 522), "FIVE STORIES THAT DEFINED THE DAY",
           font=hdr_f, fill=INK)
    d.line([mx, 548, W - mx, 548], fill=RED, width=3)

    # --- the big five: full-width rows, huge type ----------------------
    y = 560
    row_h = 68
    tag_f = font(SANS_B, 14)
    head_f = font(SERIF_B, 29)
    summ_f = font(SANS, 16)
    for tag, head, summ in BIG_FIVE:
        d.text((mx, y), tag, font=tag_f, fill=RED)
        d.text((mx, y + 19), head, font=head_f, fill=INK)
        d.text((mx, y + 50), summ, font=summ_f, fill=(40, 40, 40))
        y += row_h

    # --- "also today" strip --------------------------------------------
    strip_top = y + 2
    d.line([mx, strip_top, W - mx, strip_top], fill=RED, width=2)
    also_f = font(SANS_B, 15)
    d.text((mx, strip_top + 8), "ALSO TODAY", font=also_f, fill=RED)
    col_w = (W - 2 * mx) // 2
    item_f = font(SANS, 15)
    for i, txt in enumerate(ALSO_LEFT):
        d.text((mx, strip_top + 32 + i * 22), "\u2022  " + txt,
               font=item_f, fill=INK)
    for i, txt in enumerate(ALSO_RIGHT):
        d.text((mx + col_w, strip_top + 32 + i * 22), "\u2022  " + txt,
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
