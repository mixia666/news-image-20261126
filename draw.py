#!/usr/bin/env python3
"""Draw the 26 November 2026 front page: one 1024x1024 PNG broadsheet.

Layout, top to bottom: dateline, masthead, double rule, lead kicker +
headline + deck, the woodcut hero image with caption, a rule, two columns
of three side stories each, an ALSO TODAY strip, and a sources footer.
All text is wrapped by measured pixel width so nothing overflows the page.
Deterministic: the same inputs always produce the same bytes.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 36
CONTENT_W = PAGE - 2 * MARGIN
PAPER = (248, 243, 232)
INK = (25, 25, 25)
RED = (161, 29, 33)
GREY = (107, 101, 88)
RULE = (25, 25, 25)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by measured width; returns a list of lines."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, text, y, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((PAGE - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 6


def rule(draw, x0, x1, y, weight=1):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=weight)
    return y + weight


def double_rule(draw, y):
    rule(draw, MARGIN, PAGE - MARGIN, y, 3)
    return rule(draw, MARGIN, PAGE - MARGIN, y + 6, 1) + 4


LEAD_KICKER = "STRAIT OF HORMUZ \u00b7 THE IRAN WAR"
LEAD_HEADLINE = "Two More Tankers Hit Mines in Hormuz"
LEAD_DECK = (
    "Iran's Revolutionary Guards said two more tankers \u2014 one a supertanker "
    "carrying over two million barrels of crude \u2014 exploded and caught fire "
    "after striking mines north of Oman's Khasab port, and an LNG carrier was "
    "reported ablaze too. Brent crude climbed toward $95."
)
CAPTION = (
    "A supertanker burns in the strait as smoke rises over the cliffs "
    "and a naval mine rides the swell."
)

# (kicker, headline, body) for the six side stories.
LEFT_STORIES = [
    (
        "SAUDI ARABIA",
        "Houthis Say They Hit Ras Tanura",
        "Yemen's Houthis said they struck Saudi Arabia's largest oil refinery, "
        "a second blow to Gulf energy.",
    ),
    (
        "UNITED STATES \u00b7 TRADE",
        "Trump Hits 14 Partners With Tariffs",
        "President Trump unveiled tariffs of up to 25% on 14 trading partners; "
        "Japan and India pushed back.",
    ),
    (
        "GAZA",
        "Israeli Strikes Kill Nine in Gaza",
        "Overnight strikes killed at least nine Palestinians, including a "
        "Hamas-appointed deputy minister.",
    ),
]
RIGHT_STORIES = [
    (
        "UKRAINE",
        "Russian Missiles Hit Kyiv and Odesa",
        "Russian missiles hit Kyiv and grain ships near Odesa; Trump and NATO's "
        "chief urged restraint.",
    ),
    (
        "NORTH KOREA",
        "Kim Vows to Build More Nuclear Arms",
        "Kim Jong Un showed off progress in the North's nuclear programme and "
        "vowed to build more weapons.",
    ),
    (
        "MARKETS \u00b7 ENERGY",
        "Oil Nears $95 as Gold Slides",
        "Brent crude rose to about $94.71 on the Gulf supply scare, while gold "
        "slid to 15-month lows.",
    ),
]

ALSO_TODAY = (
    "A second U.S. judge blocks Trump's birthright citizenship order \u00b7 "
    "New York postpones the 100th Macy's Thanksgiving Day Parade as a huge "
    "storm bears down \u00b7 Dozens dead and hurt in a Cairo Ring Road fire \u00b7 "
    "SpaceX wins U.S. approval for space data centres \u00b7 U.S. famine "
    "monitor halts reporting as funding runs out \u00b7 Myanmar rejects parts "
    "of the world court's genocide ruling"
)
SOURCES = (
    "Reporting: Reuters \u00b7 Arab News \u00b7 The Japan Times \u00b7 SCMP \u00b7 "
    "The Economic Times \u00b7 Open Chronicle"
)


def draw_column(draw, stories, x, width, y):
    kicker_f = font(SANS_BOLD, 15)
    head_f = font(SERIF_BOLD, 21)
    body_f = font(SERIF, 16)
    for kicker, headline, body in stories:
        y = draw_lines(draw, [kicker], x, y, kicker_f, RED, 21)
        head_lines = wrap(draw, headline, head_f, width)
        y = draw_lines(draw, head_lines, x, y, head_f, INK, 26)
        body_lines = wrap(draw, body, body_f, width)
        y = draw_lines(draw, body_lines, x, y, body_f, INK, 22)
        y += 7
    return y


def build():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)

    y = 20
    y = centred(
        draw,
        "THURSDAY \u00b7 26 NOVEMBER 2026 \u00b7 ONE PAGE, THE WHOLE DAY",
        y,
        font(SERIF_BOLD, 18),
        GREY,
    )
    y += 2
    y = centred(draw, "THE WORLD IN ONE DAY", y, font(SERIF_BOLD, 56), INK)
    y = double_rule(draw, y + 4)

    y += 10
    y = draw_lines(
        draw, [LEAD_KICKER], MARGIN, y, font(SANS_BOLD, 18), RED, 24
    )
    head_f = font(SERIF_BOLD, 40)
    head_lines = wrap(draw, LEAD_HEADLINE, head_f, CONTENT_W)
    if len(head_lines) > 2:
        raise SystemExit("lead headline needs more than two lines")
    y = draw_lines(draw, head_lines, MARGIN, y, head_f, INK, 48)
    y += 4
    deck_f = font(SERIF, 20)
    deck_lines = wrap(draw, LEAD_DECK, deck_f, CONTENT_W)
    if len(deck_lines) > 4:
        raise SystemExit("lead deck needs more than four lines")
    y = draw_lines(draw, deck_lines, MARGIN, y, deck_f, INK, 26)
    print("after lead: y=%d headline_lines=%d deck_lines=%d"
          % (y, len(head_lines), len(deck_lines)), file=sys.stderr)
    y += 8

    hero = Image.open(os.path.join(HERE, "hero.png")).convert("RGB")
    hero_w, hero_h = hero.size
    target_w = 800
    target_h = round(hero_h * target_w / hero_w)
    hero = hero.resize((target_w, target_h), Image.LANCZOS)
    hero_x = (PAGE - target_w) // 2
    frame = Image.new("RGB", (target_w + 4, target_h + 4), INK)
    frame.paste(hero, (2, 2))
    page.paste(frame, (hero_x - 2, y))
    y += target_h + 4
    y += 5
    caption_f = font(SERIF, 15)
    caption_lines = wrap(draw, CAPTION, caption_f, CONTENT_W)
    y = draw_lines(draw, caption_lines, MARGIN, y, caption_f, GREY, 20)
    print("after hero: y=%d hero_h=%d caption_lines=%d"
          % (y, target_h, len(caption_lines)), file=sys.stderr)
    y += 6
    y = rule(draw, MARGIN, PAGE - MARGIN, y, 1)
    y += 10

    col_w = (CONTENT_W - 40) // 2
    col_top = y
    left_end = draw_column(draw, LEFT_STORIES, MARGIN, col_w, y)
    right_end = draw_column(
        draw, RIGHT_STORIES, MARGIN + col_w + 40, col_w, y
    )
    col_bottom = max(left_end, right_end)
    print("after columns: left_end=%d right_end=%d"
          % (left_end, right_end), file=sys.stderr)
    divider_x = MARGIN + col_w + 20
    draw.line(
        [(divider_x, col_top), (divider_x, col_bottom - 9)],
        fill=GREY,
        width=1,
    )
    y = col_bottom + 2
    y = rule(draw, MARGIN, PAGE - MARGIN, y, 1)
    y += 8
    y = draw_lines(
        draw, ["ALSO TODAY"], MARGIN, y, font(SANS_BOLD, 18), RED, 24
    )
    also_f = font(SERIF, 18)
    also_lines = wrap(draw, ALSO_TODAY, also_f, CONTENT_W)
    if len(also_lines) > 5:
        raise SystemExit("ALSO TODAY needs more than five lines")
    y = draw_lines(draw, also_lines, MARGIN, y, also_f, INK, 24)
    print("after also: y=%d also_lines=%d" % (y, len(also_lines)),
          file=sys.stderr)
    y += 8
    y = rule(draw, MARGIN, PAGE - MARGIN, y, 1)
    y += 6
    y = centred(draw, SOURCES, y, font(SERIF, 15), GREY)

    if y > PAGE - 8:
        raise SystemExit("page overflow: content ends at y=%d" % y)
    print("layout ok: content ends at y=%d" % y, file=sys.stderr)
    return page


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "entry.png"
    )
    page = build()
    page.save(out_path, format="PNG", optimize=False)
    digest = hashlib.sha256(open(out_path, "rb").read()).hexdigest()
    size = os.path.getsize(out_path)
    print("wrote %s (%d bytes, sha256 %s)" % (out_path, size, digest))
    if size > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB cap")
    if page.size != (1024, 1024):
        raise SystemExit("entry.png is not 1024x1024")


if __name__ == "__main__":
    main()
