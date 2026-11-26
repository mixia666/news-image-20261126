#!/usr/bin/env python3
"""Draw "The World in One Day" for Thursday 26 November 2026.

A one-page broadsheet, 1024x1024 PNG, summing up the day's world news
for the make.fun news-image-20261126 entry. The front-page art
(hero.png, kept beside this file) is an AI-generated woodcut-style
illustration of the lead story; every headline and paragraph below was
reported on 26 November 2026 (Reuters, Arab News, The Japan Times,
SCMP, The Economic Times, Open Chronicle). Deterministic: the same
inputs give the same bytes every run.

Run:  python3 draw.py            (writes entry.png beside this file)
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 245, 238)
INK = (21, 20, 18)
GREY = (92, 86, 76)
RED = (163, 28, 28)
RULE = (35, 33, 30)
FAINT = (168, 160, 146)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 36                 # side margin
X1 = W - MX             # right edge of the text block
CW = X1 - MX            # column width


def hline(y, x0=MX, x1=X1, w=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def centered(text, y, fnt, fill=INK):
    tw = d.textlength(text, font=fnt)
    d.text(((W - tw) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def block(text, x, y, fnt, max_w, leading, fill=INK):
    for ln in wrap(text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def story(x, y, col_w, kicker, head, body):
    d.text((x, y), kicker, font=F(SANS_B, 13), fill=RED)
    y += 18
    y = block(head, x, y, F(SERIF_B, 22), col_w, 25)
    y += 2
    y = block(body, x, y, F(SERIF, 16), col_w, 20, fill=(45, 42, 38))
    return y


# ---- masthead -------------------------------------------------------------
y = 22
y = centered("THURSDAY · 26 NOVEMBER 2026 · ONE PAGE, THE WHOLE DAY",
             y, F(SANS_B, 15), fill=GREY)
y += 6
y = centered("THE WORLD IN ONE DAY", y, F(SERIF_B, 54))
y += 8
hline(y, w=3)
y += 4
hline(y, w=1)
y += 13

# ---- lead -----------------------------------------------------------------
d.text((MX, y), "STRAIT OF HORMUZ · THE IRAN WAR", font=F(SANS_B, 14), fill=RED)
y += 22
y = block("Two More Tankers Hit Mines in Hormuz", MX, y, F(SERIF_B, 52), CW, 58)
y += 2
y = block("Iran's Revolutionary Guards said two more tankers — one a "
          "supertanker carrying over two million barrels of crude — "
          "exploded and caught fire after striking mines north of Oman's "
          "Khasab port, and an LNG carrier was reported ablaze too. "
          "Brent crude climbed toward $95.",
          MX, y, F(SERIF, 19), CW, 24, fill=(45, 42, 38))
y += 10

# ---- front-page art ---------------------------------------------------------
art = Image.open("hero.png").convert("RGB")
img.paste(art, (MX, y))
d.rectangle([MX, y, MX + art.width - 1, y + art.height - 1], outline=RULE, width=2)
y += art.height + 6
y = block("A supertanker burns in the strait as smoke rises over the "
          "cliffs and a naval mine rides the swell.",
          MX, y, F(SANS, 13), CW, 16, fill=GREY)
y += 8
hline(y, w=2)
y += 12

# ---- two columns ------------------------------------------------------------
GUT = 28
COLW = (CW - GUT) // 2
LX, RX = MX, MX + COLW + GUT
top = y

ly = top
ly = story(LX, ly, COLW, "SAUDI ARABIA",
           "Houthis Say They Hit Ras Tanura Refinery",
           "Yemen's Houthis said they struck Saudi Arabia's largest oil "
           "refinery, the day's second blow to Gulf energy after the "
           "mine strikes in the strait.")
ly += 11
ly = story(LX, ly, COLW, "UNITED STATES · TRADE",
           "Trump Hits 14 Partners With New Tariffs",
           "President Trump unveiled tariffs of up to 25% on 14 trading "
           "partners, accusing them of flooding markets with excess "
           "output; Japan and India pushed back.")
ly += 11
ly = story(LX, ly, COLW, "GAZA",
           "Israeli Strikes Kill Nine in Gaza",
           "Overnight airstrikes and gunfire killed at least nine "
           "Palestinians, medics said, including the Hamas-appointed "
           "deputy education minister.")

ry = top
ry = story(RX, ry, COLW, "UKRAINE",
           "Russia's Missiles Hit Kyiv and Grain Ships",
           "Russian ballistic missiles struck Kyiv, wounding seven, and "
           "hit grain ships near Odesa; Trump and NATO's chief urged "
           "Moscow not to widen the war.")
ry += 11
ry = story(RX, ry, COLW, "NORTH KOREA",
           "Kim Vows to Build More Nuclear Arms",
           "Kim Jong Un showed off progress in the North's nuclear "
           "programme and vowed to build more weapons, brushing aside "
           "President Trump's overtures.")
ry += 11
ry = story(RX, ry, COLW, "MARKETS · ENERGY",
           "Oil Nears $95 as Gold Slides",
           "Brent crude rose to about $94.71 on the Gulf supply scare, "
           "while gold slid to 15-month lows as U.S. rate-hike bets "
           "grew.")

y = max(ly, ry) + 10
d.line([(MX + COLW + GUT // 2, top), (MX + COLW + GUT // 2, y - 16)],
       fill=FAINT, width=1)

# ---- also today -------------------------------------------------------------
hline(y, w=2)
y += 9
d.text((MX, y), "ALSO TODAY", font=F(SANS_B, 14), fill=RED)
y += 20
y = block("A second U.S. judge blocks Trump's new birthright citizenship "
          "order · New York postpones the 100th Macy's Thanksgiving Day "
          "Parade as a huge storm bears down · Dozens dead and hurt in a "
          "Cairo Ring Road fire · SpaceX wins U.S. approval to launch "
          "space data centres · U.S. famine monitor halts reporting as "
          "funding runs out · Myanmar rejects parts of the world court's "
          "genocide ruling",
          MX, y, F(SERIF, 16), CW, 21, fill=(45, 42, 38))
y += 9
hline(y, w=1)
y += 7
centered("Reporting: Reuters · Arab News · The Japan Times · SCMP · "
         "The Economic Times · Open Chronicle", y, F(SANS, 13), fill=GREY)

assert y + 30 <= H, f"page overflow: content ends at {y}"
img.quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(
    "entry.png", optimize=True)
print("wrote entry.png, content ends at y =", y)
