#!/usr/bin/env python3
"""Compose the entry image for make.fun's news-image-20261117, version 2.

The page is a one-sheet newspaper front page, "The World in One Day", that
sums up Tuesday 17 November 2026 in fifty stories:

  * a masthead naming the day in large type,
  * ten hot stories with flat editorial illustration panels (a wide lead
    plus a three-by-three grid),
  * the remaining forty stories as a dense two-column numbered list.

Everything textual is rendered here with PIL and DejaVu fonts, so no letter
in the image is machine-painted guesswork. The panels are illustrations
generated for this entry and shipped beside this script as panel-*.png.

Run:  python3 compose.py     (writes entry.png next to this script)
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- canvas ---
PAGE = 1024
MARGIN = 26
CONTENT_X = MARGIN
CONTENT_W = PAGE - 2 * MARGIN  # 972
BOTTOM = PAGE - 12

PAPER = (246, 241, 229)
INK = (26, 22, 17)
ACCENT = (140, 43, 29)
MUTED = (92, 83, 71)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# ------------------------------------------------------------- typography --
_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def fit_font(draw, s, path, start, max_w, floor=10):
    """Largest font at or below start whose rendering of s fits max_w."""
    size = start
    while size > floor and text_w(draw, s, font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def wrap(draw, s, fnt, max_w):
    """Greedy word wrap; returns the list of lines."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, s, fnt, fill):
    draw.text((cx - text_w(draw, s, fnt) / 2, y), s, font=fnt, fill=fill)


def draw_tracked(draw, cx, y, s, fnt, fill, tracking):
    """Draw letterspaced text centred on cx; tracking is extra px per char."""
    widths = [text_w(draw, ch, fnt) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def rule(draw, y, height, fill=INK):
    draw.rectangle([CONTENT_X, y, CONTENT_X + CONTENT_W, y + height - 1],
                   fill=fill)
    return y + height


def paste_panel(canvas, name, box):
    """Fit the named panel into box (x, y, w, h) and frame it in ink."""
    x, y, w, h = box
    img = Image.open(os.path.join(HERE, name)).convert("RGB")
    canvas.paste(ImageOps.fit(img, (w, h)), (x, y))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


# ----------------------------------------------------------------- data ----
LEAD = ("panel-bridge.png",
        "UKRAINE STRIKES THE KERCH BRIDGE",
        "Crimea\u2013Russia link partly collapses in a missile and drone attack")

GRID = [
    ("panel-tanker.png", "TANKER HIT BY MINE IN HORMUZ"),
    ("panel-zaporizhzhia.png", "RUSSIAN STRIKE KILLS 40 IN ZAPORIZHZHIA"),
    ("panel-gaza.png", "WEST URGES ISRAEL: OPEN GAZA CROSSINGS"),
    ("panel-climate.png", "COP31 DRAFT: END FOSSIL FUELS FASTER"),
    ("panel-jets.png", "JAPAN SCRAMBLES JETS AT RUSSIAN AIRCRAFT"),
    ("panel-summit.png", "XI, TRUMP, PUTIN SUMMIT SET FOR SHENZHEN"),
    ("panel-measles.png", "US LOSES MEASLES-FREE STATUS"),
    ("panel-france.png", "146,000 MARCH AS FRANCE STRIKES"),
    ("panel-nvidia.png", "NVIDIA CHIP-SPY SCANDAL SHAKES AI RACE"),
]

LIST_LINES = [
    ("UKRAINE", "Aid-centre attack kills 26; peace talks stall"),
    ("CRIMEA", "Ukrainian drone strikes kill two"),
    ("RUSSIA", "Military plane crash in Kemerovo kills 19"),
    ("RUSSIA", "Retaliatory strikes hit bridges in Kyiv"),
    ("MOLDOVA", "Sandu: Russian drone crossed our airspace"),
    ("IRAN WAR", "Drone attack on US base in Bahrain stopped"),
    ("IRAN", "Revolutionary Guards seize a US drone"),
    ("IRAN", "US confirms strike on Qeshm Island"),
    ("IRAN", "Foreign minister in Oman for Hormuz talks"),
    ("GAZA", "Strike on tents kills three in Gaza City"),
    ("GAZA", "UN: 1.7m displaced as winter emergency deepens"),
    ("WEST BANK", "Settler mob kills Palestinian woman, 72"),
    ("ISRAEL", "E1 settlement tender suspended; new speaker"),
    ("YEMEN", "Houthis advance as army quits Red Sea coast"),
    ("YEMEN", "Saudi strike kills seven in Hudaydah factory"),
    ("IRAQ", "Kata'ib Hezbollah warns troops over Jurf al-Sakhar"),
    ("CHINA", "APEC leaders' week opens in Shenzhen"),
    ("NORTH KOREA", "Trump eyes Kim meeting at APEC"),
    ("MONGOLIA", "President resigns amid corruption scandal"),
    ("ASIA", "Quad leaders reaffirm Indo-Pacific commitment"),
    ("US", "Pentagon fails its audit for a ninth straight year"),
    ("US", "NSA internal network crash disrupts operations"),
    ("US", "Trump 'looking into' Iran dirty-bomb claim"),
    ("US", "Ship collision in New Orleans after steering failure"),
    ("FRANCE", "Depardieu drops appeal, admits assault charges"),
    ("EUROPE", "EU\u2013Rwanda migrant return-hub plan sparks row"),
    ("SERBIA", "Pilot killed in military jet crash"),
    ("T\u00dcRK\u0130YE", "AI climate pledge launched at COP31"),
    ("ERITREA", "WHO confirms trachoma eliminated"),
    ("SOUTH AFRICA", "17 killed in two mass shootings"),
    ("LIBYA", "4.1-magnitude earthquake off the coast"),
    ("THAILAND", "Phuket fire kills 11"),
    ("HAITI", "Protests back Salvadoran military operation"),
    ("PAKISTAN", "Petrol and diesel cut by Rs2 a litre"),
    ("PAKISTAN", "ECO summit adopts Vision 2035 in Islamabad"),
    ("TECH", "US tightens global AI chip export controls"),
    ("MARKETS", "Brent steady near $92.61 on Hormuz fears"),
    ("CRYPTO", "Bitcoin stalls below $65,000 after selloff"),
    ("SPORT", "India edge Pakistan in U19 Asia Cup final"),
    ("SPORT", "Germany thrash Netherlands 5\u20130"),
]

# --------------------------------------------------------------- sections --
TITLE_SIZE = 27
DATE_START = 56
STRAP_SIZE = 20
LEAD_IMG_H = 86
LEAD_HEAD_SIZE = 31
LEAD_SUB_SIZE = 19
GRID_IMG_H = 56
GRID_HEAD_SIZE = 17
GRID_HEAD_LH = 20
LIST_HEAD_SIZE = 20
LIST_FONT_SIZE = 14


def masthead(draw, page, y):
    cx = PAGE // 2
    y = rule(draw, y, 4)
    y += 6
    draw_centered(draw, cx, y, "THE WORLD IN ONE DAY",
                  font(SERIF_BOLD, TITLE_SIZE), INK)
    y += 34
    date_font = fit_font(draw, "TUESDAY 17 NOVEMBER 2026", SERIF_BOLD,
                         DATE_START, CONTENT_W)
    print("date set at %d px" % date_font.size)
    draw_centered(draw, cx, y, "TUESDAY 17 NOVEMBER 2026", date_font, INK)
    y += int(date_font.size * 1.18)
    draw_tracked(draw, cx, y, "THE DAY IN 50 STORIES",
                 font(SANS_BOLD, STRAP_SIZE), ACCENT, tracking=3)
    y += 26
    y = rule(draw, y + 4, 2)
    return y


def lead(draw, page, y):
    y += 8
    paste_panel(page, LEAD[0], (CONTENT_X, y, CONTENT_W, LEAD_IMG_H))
    y += LEAD_IMG_H + 5
    draw.text((CONTENT_X, y), LEAD[1], font=font(SERIF_BOLD, LEAD_HEAD_SIZE),
              fill=INK)
    y += 38
    draw.text((CONTENT_X, y), LEAD[2], font=font(SANS, LEAD_SUB_SIZE),
              fill=MUTED)
    y += 25
    return y


def hot_grid(draw, page, y):
    y += 8
    cols, gutter = 3, 14
    cell_w = (CONTENT_W - (cols - 1) * gutter) // cols
    head_font = font(SANS_BOLD, GRID_HEAD_SIZE)
    cell_h = GRID_IMG_H + 3 + 2 * GRID_HEAD_LH
    for i, (panel, headline) in enumerate(GRID):
        row, col = divmod(i, cols)
        x = CONTENT_X + col * (cell_w + gutter)
        top = y + row * (cell_h + 8)
        paste_panel(page, panel, (x, top, cell_w, GRID_IMG_H))
        lines = wrap(draw, headline, head_font, cell_w)[:2]
        for j, line in enumerate(lines):
            draw.text((x, top + GRID_IMG_H + 3 + j * GRID_HEAD_LH), line,
                      font=head_font, fill=INK)
    return y + 3 * cell_h + 2 * 8


TRUNCATED = []


def list_section(draw, y):
    y += 8
    y = rule(draw, y, 2)
    y += 5
    draw.text((CONTENT_X, y), "40 MORE STORIES OF THE DAY",
              font=font(SANS_BOLD, LIST_HEAD_SIZE), fill=INK)
    y += 31

    rows = (len(LIST_LINES) + 1) // 2
    line_h = (BOTTOM - y) / rows
    f_num = font(SANS_BOLD, LIST_FONT_SIZE)
    f_tag = font(SANS_BOLD, LIST_FONT_SIZE)
    f_head = font(SANS, LIST_FONT_SIZE)
    num_w = text_w(draw, "40.", f_num) + 5
    gutter = 20
    col_w = (CONTENT_W - gutter) // 2
    print("list: %d rows, line height %.2f px at %d px font"
          % (rows, line_h, LIST_FONT_SIZE))

    for i, (tag, headline) in enumerate(LIST_LINES):
        col, row = divmod(i, rows)
        x = CONTENT_X + col * (col_w + gutter)
        top = y + row * line_h
        draw.text((x, top), "%d." % (i + 1), font=f_num, fill=ACCENT)
        tx = x + num_w
        draw.text((tx, top), tag, font=f_tag, fill=INK)
        tx += text_w(draw, tag, f_tag)
        draw.text((tx, top), " \u2014 ", font=f_head, fill=MUTED)
        tx += text_w(draw, " \u2014 ", f_head)
        avail = x + col_w - tx
        shown = headline
        if text_w(draw, shown, f_head) > avail:
            while shown and text_w(draw, shown + "\u2026", f_head) > avail:
                shown = shown[:-1]
            shown = shown.rstrip() + "\u2026"
            TRUNCATED.append((i + 1, headline))
        draw.text((tx, top), shown, font=f_head, fill=INK)
    if TRUNCATED:
        print("list lines truncated to fit:", TRUNCATED)
    else:
        print("list: every headline fits its column untruncated")
    return y + rows * line_h


def build():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)
    y = 14
    y = masthead(draw, page, y)
    print("after masthead: y =", y)
    y = lead(draw, page, y)
    print("after lead:     y =", y)
    y = hot_grid(draw, page, y)
    print("after grid:     y =", y)
    y = list_section(draw, y)
    print("after list:     y = %.1f (page bottom %d)" % (y, BOTTOM))
    return page


def save(page):
    out = os.path.join(HERE, "entry.png")
    page.save(out, optimize=True)
    size = os.path.getsize(out)
    print("entry.png: %d bytes" % size)
    if size > 950_000:
        small = page.quantize(colors=256, method=Image.MEDIANCUT)
        small.save(out, optimize=True)
        size = os.path.getsize(out)
        print("quantized to 256 colours: %d bytes" % size)
    if size > 1_048_576:
        page.resize((960, 960), Image.LANCZOS).save(out, optimize=True)
        size = os.path.getsize(out)
        print("resized to 960: %d bytes" % size)
    preview = page.resize((300, 300), Image.LANCZOS)
    preview.save("/tmp/news-image-v2-preview300.png")
    print("preview written to /tmp/news-image-v2-preview300.png")


if __name__ == "__main__":
    save(build())
