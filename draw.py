#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261120 entry.

Draws entry.png (900x1024) with Pillow. This script runs ONLY on the
build machine; the grader runs main.py, which is standard library
only and just copies the committed entry.png.

Every story below was first reported on Friday 20 November 2026
(or happened that day), verified against live news sources during
the build session.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (253, 253, 248)
INK = (17, 17, 17)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
GREY = (90, 90, 86)
LIGHT_GREY = (220, 220, 212)
TAG_BG = (238, 238, 230)

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


def draw_globe(draw, cx, cy, r, color):
    """Simple line globe: circle, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=color, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
             fill=color, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 20, 160,
             fill=color, width=2)


# (tag, headline, summary) — 2 lead stories, then 33 in the grid.
LEADS = [
    ("UNITED STATES",
     "TRUMP PUSHES IRAN WAR DECISION TO 2027",
     "President Trump says there is \u201cno rush\u201d on Iran and he will "
     "\u201csee what happens\u201d after January 1."),
    ("INTERNATIONAL COURT OF JUSTICE",
     "MYANMAR COMMITTED GENOCIDE, UN COURT RULES",
     "The ICJ rules 9\u20136 that Myanmar committed genocide against the "
     "Rohingya in the 2017 crackdown."),
]

STORIES = [
    ("MIDDLE EAST",
     "Houthi missiles strike Riyadh",
     "Missiles hit King Khalid airport and the PIF tower."),
    ("UKRAINE",
     "Europe ready for talks with Russia",
     "Leaders say they are ready to negotiate an end to the war."),
    ("UKRAINE",
     "Russian strikes hit Kyiv embassies",
     "Strikes damage the Austrian and Dutch embassies in Kyiv."),
    ("MARKETS",
     "Russian markets slump after summit",
     "Stocks fall after the summit ends with no Ukraine deal."),
    ("UNITED STATES",
     "Trump to face press at noon",
     "Back from China, Trump holds a White House news conference."),
    ("CHINA",
     "Three nuclear powers, one table",
     "Trump, Xi and Putin hold a first-ever three-way summit."),
    ("UNITED STATES",
     "Jeffries set to be first Black Speaker",
     "Democrats nominate Hakeem Jeffries to be House Speaker."),
    ("INDIA",
     "Judge Varma resigns over cash row",
     "Justice Varma quits, saying it is no admission of guilt."),
    ("UNITED STATES",
     "Election-security pick denies Jan 6",
     "Trump's pick denies January 6 was an attack on the Capitol."),
    ("SOUTH KOREA",
     "Ex-PM's martial-law conviction quashed",
     "The Supreme Court overturns Han Duck-soo's conviction."),
    ("PACIFIC",
     "Fiji declares national disaster",
     "Severe drought and water shortages driven by El Ni\u00f1o."),
    ("UKRAINE",
     "Crimean Bridge rail link disrupted",
     "A Ukrainian attack halts rail traffic to Crimea."),
    ("NORTH KOREA",
     "Yongbyon enrichment expanding",
     "The UN watchdog reports expansion at Yongbyon."),
    ("AMERICAS",
     "US and Venezuela restore military ties",
     "Washington and Caracas sign a military cooperation deal."),
    ("BANGLADESH",
     "Fire at Yunus ancestral home",
     "A fire at ex-leader Yunus's home; arson is suspected."),
    ("INDIA",
     "Modi meets William and Kate",
     "PM Modi meets the royal couple in New Delhi."),
    ("SPACE",
     "Hayabusa2 drops asteroid landing",
     "Engine trouble forces Japan's probe to change plans."),
    ("GAMING",
     "GTA VI sales pass $1.8 billion",
     "GTA VI already outsells The Odyssey's $1.80bn run."),
    ("TECH",
     "Anthropic IPO closes today",
     "The $83-a-share listing values the AI firm at ~$1.5tn."),
    ("TECH",
     "Google ships Gemini 4 Neon",
     "Google's new model tops AI benchmarks."),
    ("TECH",
     "Nvidia guides to $130bn quarter",
     "Nvidia forecasts $130bn in sales; Huang will not return."),
    ("MARKETS",
     "Sensex surges 1,000 points",
     "India's Sensex closes at 83,022; Nifty tops 25,500."),
    ("CRICKET",
     "Nicholls' 113 lifts New Zealand",
     "Nicholls hits 113 not out; NZ reach 243 for 5, day one."),
    ("FOOTBALL",
     "India beat Pakistan 2-1 for SAFF title",
     "India win a record 10th SAFF Championship."),
    ("CRICKET",
     "Bavuma ruled out of Test decider",
     "South Africa's captain misses the Bangladesh decider."),
    ("CHESS",
     "Carlsen forfeit row rocks chess",
     "Carlsen's shock forfeit stirs a favouritism row."),
    ("CINEMA",
     "Ramayana ticket prices slashed",
     "Cinemas cut prices from today; film nears Rs 800 crore."),
    ("INDIA",
     "NEET leak: charges against 14",
     "A Delhi court orders charges in the NEET-UG leak case."),
    ("DEFENCE",
     "India-Israel Rs 1,976 cr missile deal",
     "Deal to upgrade the Navy's Barak missile system."),
    ("YEMEN",
     "64 children killed in Yemen fighting",
     "UNICEF: 64 children killed as fighting displaces 330,000."),
]

# One-line items in the "Also today" strip at the bottom.
ALSO = [
    "Jacksonville flood watch: up to 10 in. of rain",
    "COP31 talks continue in T\u00fcrkiye",
    "World Children's Day",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top red rule -------------------------------------------------
    d.rectangle([0, 0, W, 7], fill=RED)

    # --- masthead -----------------------------------------------------
    mx = 24
    draw_globe(d, 62, 62, 26, INK)
    title_f = font(SERIF_B, 52)
    d.text((100, 22), "THE WORLD IN ONE DAY", font=title_f, fill=INK)
    d.line([mx, 92, W - mx, 92], fill=INK, width=2)
    date_f = font(SANS_B, 24)
    date_txt = "FRIDAY  \u2022  20 NOVEMBER 2026  \u2022  THE DAY'S NEWS IN ONE IMAGE"
    tw = d.textlength(date_txt, font=date_f)
    d.text(((W - tw) / 2, 100), date_txt, font=date_f, fill=RED)

    # --- lead stories -------------------------------------------------
    lead_top = 128
    lead_h = 124
    col_w = (W - 2 * mx - 16) // 2
    for i, (tag, head, summ) in enumerate(LEADS):
        x0 = mx + i * (col_w + 16)
        d.rectangle([x0, lead_top, x0 + col_w, lead_top + lead_h],
                    outline=INK, width=2)
        d.rectangle([x0, lead_top, x0 + col_w, lead_top + 24], fill=INK)
        tag_f = font(SANS_B, 12)
        d.text((x0 + 8, lead_top + 5), tag, font=tag_f, fill=PAPER)
        head_f = font(SERIF_B, 21)
        lines = wrap(d, head, head_f, col_w - 16)
        y = lead_top + 30
        for ln in lines[:2]:
            d.text((x0 + 8, y), ln, font=head_f, fill=INK)
            y += 25
        summ_f = font(SANS, 13)
        for ln in wrap(d, summ, summ_f, col_w - 16)[:2]:
            d.text((x0 + 8, y), ln, font=summ_f, fill=(40, 40, 40))
            y += 17

    # --- grid header --------------------------------------------------
    gy = lead_top + lead_h + 12
    d.line([mx, gy, W - mx, gy], fill=RED, width=3)
    hdr_f = font(SANS_B, 15)
    d.text((mx, gy + 6), "THE DAY IN BRIEF  \u2014  30 MORE STORIES FROM AROUND THE WORLD",
           font=hdr_f, fill=INK)
    gy += 30

    # --- story grid: 3 columns x 10 rows -----------------------------
    gap = 10
    cols = 3
    rows = 10
    cw = (W - 2 * mx - (cols - 1) * gap) // cols
    strip_top = H - 52
    rh = (strip_top - gy) // rows
    tag_f = font(SANS_B, 10)
    head_f = font(SANS_B, 13)
    summ_f = font(SANS, 11)
    for idx, (tag, head, summ) in enumerate(STORIES):
        r, c = divmod(idx, cols)
        x0 = mx + c * (cw + gap)
        y0 = gy + r * rh
        d.rectangle([x0, y0, x0 + cw, y0 + rh - 4], fill=TAG_BG)
        d.text((x0 + 6, y0 + 3), tag, font=tag_f, fill=RED)
        y = y0 + 17
        for ln in wrap(d, head, head_f, cw - 12)[:2]:
            d.text((x0 + 6, y), ln, font=head_f, fill=INK)
            y += 16
        # summary: only lines that fit inside the card, with ellipsis
        avail = (y0 + rh - 6) - y
        max_lines = max(0, avail // 13)
        slines = wrap(d, summ, summ_f, cw - 12)
        for j, ln in enumerate(slines[:max_lines]):
            if j == max_lines - 1 and len(slines) > max_lines:
                while ln and d.textlength(ln + "\u2026", font=summ_f) > cw - 12:
                    ln = ln[:-1]
                ln = ln + "\u2026"
            d.text((x0 + 6, y), ln, font=summ_f, fill=(50, 50, 50))
            y += 13

    # --- "also today" strip ------------------------------------------
    d.line([mx, strip_top, W - mx, strip_top], fill=RED, width=2)
    also_f = font(SANS_B, 12)
    also_txt = "ALSO TODAY:  " + "   \u2022   ".join(ALSO)
    d.text((mx, strip_top + 6), also_txt, font=also_f, fill=INK)

    # --- footer -------------------------------------------------------
    d.line([mx, H - 26, W - mx, H - 26], fill=LIGHT_GREY, width=1)
    foot_f = font(SANS, 11)
    foot = ("All stories first reported on 20 November 2026  \u2022  "
            "Sources: Reuters, BBC, NYT, AFP, AP, NDTV, The Hindu")
    tw = d.textlength(foot, font=foot_f)
    d.text(((W - tw) / 2, H - 21), foot, font=foot_f, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("wrote %s %dx%d %d bytes" % (OUT, W, H, size))
    assert size <= 1048576, "image over 1 MiB"


if __name__ == "__main__":
    main()
