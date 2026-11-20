"""Build-time compositor for news-image-20261120 v1.

Build-time only (uses Pillow). The graded entrypoint is main.py, which is
stdlib-only and simply copies the finished entry.png. Run:
    python3 build.py
Produces entry.png (JPEG bytes, 1024x1024, <= 1 MiB) in this directory.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (178, 30, 30)
NAVY = (30, 58, 95)
MUTED = (110, 108, 100)
RULE = (196, 188, 172)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(size, bold=False, serif=False, italic=False):
    if serif:
        if bold and italic:
            name = "LiberationSerif-BoldItalic.ttf"
        elif bold:
            name = "LiberationSerif-Bold.ttf"
        elif italic:
            name = "LiberationSerif-Italic.ttf"
        else:
            name = "LiberationSerif-Regular.ttf"
    else:
        if bold and italic:
            name = "LiberationSans-BoldItalic.ttf"
        elif bold:
            name = "LiberationSans-Bold.ttf"
        elif italic:
            name = "LiberationSans-Italic.ttf"
        else:
            name = "LiberationSans-Regular.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def crop_to(img, tw, th):
    """Center-crop an image to the target aspect, then resize."""
    sw, sh = img.size
    target = tw / th
    src = sw / sh
    if src > target:  # too wide: crop sides
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, sh))
    else:  # too tall: crop top/bottom (bias slightly up)
        nh = int(sw / target)
        y0 = max(0, (sh - nh) // 2 - int(0.06 * sh))
        img = img.crop((0, y0, sw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def paste_photo(page, path, x, y, w, h, radius=5):
    img = Image.open(os.path.join(ASSETS, path)).convert("RGB")
    img = crop_to(img, w, h)
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    page.paste(img, (x, y), mask)
    d = ImageDraw.Draw(page)
    d.rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=radius,
                        outline=INK, width=1)


# ---------------------------------------------------------------- data
# (num, image, tag, headline, summary, source, lon, lat) — lon/lat for map.
FEATURES = [
    (1, "f01.jpg", "ASIA-PACIFIC · INDIA",
     "AKVAN SLAMS ODISHA",
     "Cyclone makes landfall near Gopalpur; 300,000+ evacuated and 9,341 shelters opened.",
     "IMD / Reuters", 85.5, 19.5),
    (2, "f02.jpg", "EUROPE · UKRAINE",
     "KYIV BRIDGES HIT IN NIGHT ATTACK",
     "Ballistic missiles damage 3 Dnipro bridges; 3 killed, about 15 hurt; fires across the city.",
     "Kyiv Independent", 30.5, 50.4),
    (3, "f03.jpg", "WORLD · ANTALYA",
     "COP31 ENDS IN DEADLOCK",
     "Final text drops fossil-fuel language; 21 issues unresolved as talks run past midnight.",
     "UN News", 30.7, 36.9),
    (4, "f04.jpg", "ASIA-PACIFIC · MARKETS",
     "ASIA SHARES PLUNGE",
     "Nikkei -4.1%, Kospi -4.7%; worst week since 2020.",
     "Reuters", 139.7, 35.7),
    (5, "f05.jpg", "ASIA-PACIFIC · JAPAN",
     "JAPAN PRICES UP 2.3%",
     "Oct CPI 2.3%; a BoJ rate rise looks near.",
     "Reuters", 146.5, 40.5),
    (6, "f06.jpg", "OCEANIA · CRICKET",
     "PHILLIPS HITS 118",
     "NZ recover from 70/5; century lifts them to 368.",
     "Sportradar", 174.8, -41.3),
    (7, "f07.jpg", "AMERICAS · LAS VEGAS",
     "RUSSELL FASTEST IN THE WET",
     "Wet FP2: Russell 1:47.272; FP1 washed out.",
     "formula1.com", -115.1, 36.2),
    (8, "f08.jpg", "AMERICAS · BRAZIL",
     "RAONI'S LAND RECOGNISED",
     "Brazil recognises Chief Raoni's ancestral land.",
     "Brazil govt", -55.0, -12.0),
    (9, "f09.jpg", "EUROPE · TURKEY",
     "TURKEY CHOPPER DOWN, 4 DEAD",
     "Military helicopter crashes in Malatya; 4 dead.",
     "Turkish media", 38.3, 38.4),
    (10, "f10.jpg", "EUROPE · LONDON",
     "UK SENDS 1,000 DRONES",
     "London pledges 1,000+ drones, \u00a3260m for Kyiv.",
     "UK govt", -0.1, 51.5),
    (11, "f11.jpg", "MIDEAST · GAZA",
     "GAZA LINE CROSSED",
     "Israeli forces cross the Yellow Line in Gaza.",
     "News wires", 34.5, 31.5),
    (12, "f12.jpg", "SPACE · MERCURY",
     "MERCURY'S BIG WEEKEND",
     "Best evening showing Fri; capture starts Sat.",
     "ESA", None, None),
    (13, "f13.jpg", "AFRICA · ZIMBABWE",
     "250,000 MINES DESTROYED",
     "HALO Trust destroys 250,000 landmines.",
     "HALO Trust", 30.0, -19.0),
    (14, "f14.jpg", "AFRICA · SENEGAL",
     "SENEGAL BOAT CAPSIZES",
     "Migrant boat capsizes; 4 dead, dozens missing.",
     "Local media", -17.4, 14.7),
]

STATS = [
    ("300,000+", "EVACUATED AS AKVAN HIT"),
    ("3", "KYIV BRIDGES DAMAGED"),
    ("-4.1%", "NIKKEI'S FRIDAY FALL"),
    ("2.3%", "JAPAN OCTOBER CPI"),
    ("118", "PHILLIPS' WELLINGTON TON"),
    ("250,000", "LANDMINES DESTROYED"),
]

CHIPS = [
    ("EUROPE", 9), ("AMERICAS", 10), ("ASIA-PACIFIC", 6),
    ("MIDEAST", 4), ("AFRICA", 4), ("OCEANIA", 3), ("WORLD / SPACE", 2),
]

BRIEFS = [
    (15, "Sudan gold-mine drone strike kills 10"),
    (16, "US, Venezuela sign military cooperation deal"),
    (17, "Mosque torched in al-Dahi, northern Israel"),
    (18, "Violence in Bangladesh ahead of Hasina return"),
    (19, "Iraq orders Iran-backed militia out of town"),
    (20, "IAEA: North Korea expanding uranium enrichment"),
    (21, "Brazil central bank sells $1bn to steady real"),
    (22, "Spain campaign opens; S\u00e1nchez admits errors"),
    (23, "Italy beat France 3-1 in Nations League"),
    (24, "Rosal\u00eda makes Latin Grammy history"),
    (25, "Scaloni extends Argentina deal to 2030"),
    (26, "Alcaraz cleared for Cobolli; Sinner 3-0"),
    (27, "Cyclone Xavier warnings for Cook Islands"),
    (28, "Fujairah crash kills 14, injures 30"),
    (29, "China holds loan prime rate steady"),
    (30, "US reporters told to bag phones on China flight"),
    (31, "Malawi fuel crisis sparks violence"),
    (32, "Czech leaders visit Israel, deepen defence ties"),
    (33, "US sanctions Comancheros and 'Ndrangheta"),
    (34, "Youth strike in 25+ nations over living costs"),
    (35, "US court curbs agriculture chief's faith emails"),
    (36, "Poland inks $50bn nuclear deal with US firms"),
    (37, "Meta revises 2030 climate goals as AI grows"),
    (38, "Australia urged to drop faith from terror law"),
]

DATE_CHECK = [
    "ICJ: Myanmar guilty of Rohingya genocide \u2014 Thu 19 Nov",
    "Trump\u2013Xi\u2013Putin summit in Shenzhen \u2014 Thu 19 Nov",
    "Houthi missile hits Riyadh tower \u2014 Thu 19 Nov",
    "US Senate rejects Iran war-powers bill \u2014 Thu 19 Nov",
    "Denmark backs Greenland defence deal \u2014 Thu 19 Nov",
    "Microsoft explains its 12 Nov outage \u2014 Thu 19 Nov",
]

SOURCES_LINE = ("38 STORIES \u00b7 6 CONTINENTS \u00b7 SOURCES: Reuters, AP, AFP, BBC, "
                "IMD, UN News, Al Jazeera, Kyiv Independent, formula1.com, ESA, "
                "HALO Trust, Morningstar")


# ---------------------------------------------------------------- drawing
def draw_feature(d, page, f, x, y, w, h, hero=False):
    num, img, tag, head, summ, src = f[0], f[1], f[2], f[3], f[4], f[5]
    if hero:
        ih = 96
        tag_f, head_f, sum_f, src_f = font(9, bold=True), font(15, bold=True), font(11), font(8.5)
        num_f = font(11, bold=True)
        lh, ls = 18, 14
    else:
        ih = 84
        tag_f, head_f, sum_f, src_f = font(8, bold=True), font(11, bold=True), font(9), font(8)
        num_f = font(9, bold=True)
        lh, ls = 13, 11.5
    paste_photo(page, img, x, y, w, ih)
    ty = y + ih + 5
    # number badge + tag (+ source right-aligned on the same line for heroes)
    d.ellipse([x, ty - 1, x + 15, ty + 14], fill=RED)
    d.text((x + 7.5, ty + 6.5), str(num), font=num_f, fill=WHITE, anchor="mm")
    d.text((x + 20, ty + 6), tag, font=tag_f, fill=NAVY, anchor="lm")
    if hero:
        d.text((x + w, ty + 6), src, font=src_f, fill=MUTED, anchor="rm")
    hy = ty + 17
    lines = wrap(d, head, head_f, w)
    for ln in lines[:2]:
        d.text((x, hy), ln, font=head_f, fill=INK)
        hy += lh
    sy = hy + 1
    for ln in wrap(d, summ, sum_f, w)[:2 if hero else 3]:
        d.text((x, sy), ln, font=sum_f, fill=(60, 60, 60))
        sy += ls
    if not hero:
        d.text((x, y + h - 10), "Source: " + src, font=src_f, fill=MUTED)


def build():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- masthead (0-96)
    d.rectangle([0, 0, W, 5], fill=RED)
    d.rectangle([0, 5, W, 7], fill=INK)
    kick = "T H E   W O R L D   I N   O N E   D A Y   \u00b7   3 8   S T O R I E S   \u00b7   6   C O N T I N E N T S"
    d.text((W / 2, 20), kick, font=font(10, bold=True), fill=INK, anchor="mm")
    d.text((W / 2, 52), "FRIDAY 20 NOVEMBER 2026", font=font(44, bold=True, serif=True),
           fill=INK, anchor="mm")
    sub = "Cyclone Akvan slams Odisha  \u00b7  Kyiv bridges hit  \u00b7  COP31 deadlock  \u00b7  Asia shares plunge"
    d.text((W / 2, 82), sub, font=font(13, serif=True, italic=True), fill=RED, anchor="mm")
    d.line([12, 93, W - 12, 93], fill=INK, width=2)

    # ---- stats strip (96-128)
    cw = (W - 24) / 6
    for i, (num, lab) in enumerate(STATS):
        cx = 12 + i * cw
        d.text((cx + cw / 2, 108), num, font=font(18, bold=True), fill=RED, anchor="mm")
        d.text((cx + cw / 2, 122), lab, font=font(8, bold=True), fill=MUTED, anchor="mm")
        if i:
            d.line([cx, 100, cx, 126], fill=RULE, width=1)
    d.line([12, 128, W - 12, 128], fill=RULE, width=1)

    # ---- region chips (128-150)
    chip_f = font(10, bold=True)
    widths = []
    for name, n in CHIPS:
        widths.append(d.textlength(name + "  " + str(n), font=chip_f) + 18)
    total = sum(widths) + (len(CHIPS) - 1) * 8
    cx = (W - total) / 2
    for (name, n), wd in zip(CHIPS, widths):
        d.rounded_rectangle([cx, 133, cx + wd, 147], radius=7, outline=INK, width=1, fill=WHITE)
        d.text((cx + 9, 140), name, font=chip_f, fill=INK, anchor="lm")
        d.text((cx + wd - 9, 140), str(n), font=chip_f, fill=RED, anchor="rm")
        cx += wd + 8
    d.line([12, 152, W - 12, 152], fill=INK, width=1)

    # ---- hero row (156-324): features 1-3
    hw = 330
    hx = [12, 347, 682]
    for f, x in zip(FEATURES[:3], hx):
        draw_feature(d, page, f, x, 156, hw, 168, hero=True)
    d.line([12, 328, W - 12, 328], fill=RULE, width=1)

    # ---- grid row 1 (332-507): features 4-9, 6 cols
    gw6 = 160
    gx6 = [12 + i * (gw6 + 8) for i in range(6)]
    for f, x in zip(FEATURES[3:9], gx6):
        draw_feature(d, page, f, x, 332, gw6, 175)
    d.line([12, 511, W - 12, 511], fill=RULE, width=1)

    # ---- grid row 2 (515-690): features 10-14, 5 cols
    gw5 = 193
    gx5 = [12 + i * (gw5 + 8) for i in range(5)]
    for f, x in zip(FEATURES[9:14], gx5):
        draw_feature(d, page, f, x, 515, gw5, 175)
    d.line([12, 694, W - 12, 694], fill=INK, width=1)

    # ---- map band (698-856): map left, date check right
    d.text((12, 710), "WHERE IT HAPPENED", font=font(12, bold=True), fill=INK)
    d.text((12, 724), "14 stories, 6 continents \u2014 and one planet next door",
           font=font(9, italic=True), fill=MUTED)
    mmap = Image.open(os.path.join(ASSETS, "map.jpg")).convert("RGB")
    # crop to inhabited latitudes 75..-55 (equirectangular 2240x1120)
    mw, mh = mmap.size
    y0 = int((90 - 75) / 180 * mh)
    y1 = int((90 + 55) / 180 * mh)
    mmap = mmap.crop((0, y0, mw, y1)).resize((480, 120), Image.LANCZOS)
    page.paste(mmap, (12, 734))
    d = ImageDraw.Draw(page)
    d.rectangle([12, 734, 492, 854], outline=INK, width=1)
    # pins: lon/lat -> map px (crop band lat 75..-55, 120 px tall)
    for f in FEATURES:
        lon, lat = f[6], f[7]
        if lon is None:
            continue
        px = 12 + (lon + 180) / 360 * 480
        py = 734 + (75 - lat) / 130 * 120
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=WHITE, width=1)
        d.text((px, py), str(f[0]), font=font(8, bold=True), fill=WHITE, anchor="mm")
    # Mercury note (no earthly pin)
    d.ellipse([470, 740, 484, 754], fill=RED, outline=WHITE, width=1)
    d.text((477, 747), "12", font=font(8, bold=True), fill=WHITE, anchor="mm")
    d.text((466, 760), "MERCURY", font=font(7, bold=True), fill=RED, anchor="ra")

    # date-check panel (x 512-1012)
    px0 = 512
    d.text((px0, 710), "DATE CHECK \u2014 LEFT OUT ON PURPOSE", font=font(12, bold=True), fill=RED)
    d.text((px0, 724), "First reported Thursday 19 Nov \u2014 not Friday's news:",
           font=font(9, italic=True), fill=MUTED)
    yy = 742
    for item in DATE_CHECK:
        d.text((px0, yy), "\u2022  " + item, font=font(9), fill=(60, 60, 60))
        yy += 16
    d.line([px0, yy + 2, W - 12, yy + 2], fill=RULE, width=1)
    d.text((px0, yy + 12), "BY THE NUMBERS", font=font(10, bold=True), fill=INK)
    nums = "38 stories  \u00b7  14 pictured  \u00b7  6 continents  \u00b7  0 Thursday stories inside"
    d.text((px0, yy + 28), nums, font=font(10), fill=INK)

    d.line([12, 860, W - 12, 860], fill=INK, width=1)

    # ---- briefs (864-988)
    d.text((12, 874), "ALSO ON FRIDAY \u2014 24 MORE STORIES", font=font(12, bold=True), fill=INK)
    bw = 244
    bx = [12 + i * (bw + 8) for i in range(4)]
    bf, nf = font(9.5), font(9.5, bold=True)
    for i, (n, txt) in enumerate(BRIEFS):
        col, row = i % 4, i // 4
        y = 892 + row * 16
        d.text((bx[col], y), str(n), font=nf, fill=RED)
        d.text((bx[col] + 22, y), txt, font=bf, fill=INK)

    # ---- footer (992-1024)
    d.line([12, 992, W - 12, 992], fill=RULE, width=1)
    d.text((W / 2, 1008), SOURCES_LINE, font=font(8.5), fill=MUTED, anchor="mm")

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="JPEG", quality=88, optimize=True)
    size = os.path.getsize(out)
    print("entry.png:", size, "bytes,", page.size, "JPEG-in-png-name")
    assert size <= 1_048_576, "over 1 MiB!"
    assert page.size == (1024, 1024)
    return out


if __name__ == "__main__":
    build()
