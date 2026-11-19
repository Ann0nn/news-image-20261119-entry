# Builds entry.png: a one-page newspaper front page summing up the world
# news of Thursday 19 November 2026.
#
#   python3 src/render.py   -> writes entry.png at the repository root
#
# The picture is 1024 by 1024 pixels and stays well under 1 MiB. Every
# headline on it was checked against live reporting published on 19 Nov
# 2026 (Anadolu, Reuters, Al Jazeera, Japan Times, Malay Mail, Haaretz):
# each story either happened that day or was first reported that day.

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024

PAPER = (250, 246, 236)
CARD = (255, 255, 255)
TEXT = (20, 20, 20)
SOFT = (52, 52, 52)
FAINT = (96, 96, 96)
LINE = (178, 178, 172)
SKY = (232, 238, 245)
DARK = (13, 38, 68)
SCARLET = (168, 24, 34)
GOLD = (255, 206, 62)
GLOBE_BLUE = (64, 106, 158)

DEJAVU = "/usr/share/fonts/truetype/dejavu/"


def font(kind, size):
    """Load one of the four DejaVu faces used across the page."""
    names = {
        "serif-bold": "DejaVuSerif-Bold.ttf",
        "serif": "DejaVuSerif.ttf",
        "sans-bold": "DejaVuSans-Bold.ttf",
        "sans": "DejaVuSans.ttf",
    }
    return ImageFont.truetype(DEJAVU + names[kind], size)


def fit_lines(pen, words_text, face, size, width):
    """Split words_text into lines that fit width pixels in the given face."""
    face_obj = font(face, size)
    words = words_text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if pen.textlength(candidate, font=face_obj) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_lines(pen, x, y, lines, face, size, colour, step):
    """Draw lines of text starting at (x, y); return the y below the last."""
    face_obj = font(face, size)
    for line in lines:
        pen.text((x, y), line, font=face_obj, fill=colour)
        y += step
    return y


def draw_world(pen, cx, cy, radius):
    """Decorative globe: an outline ring, latitude bands and city dots."""
    pen.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        outline=GLOBE_BLUE, width=4,
    )
    for frac in (-0.55, 0.0, 0.55):
        yy = cy + frac * radius
        half = (radius ** 2 - (frac * radius) ** 2) ** 0.5
        pen.line([cx - half, yy, cx + half, yy], fill=GLOBE_BLUE, width=3)
    pen.ellipse(
        [cx - radius * 0.55, cy - radius, cx + radius * 0.55, cy + radius],
        outline=GLOBE_BLUE, width=3,
    )
    for dx, dy in ((-0.4, -0.3), (0.25, 0.15), (0.45, -0.45), (-0.15, 0.5)):
        px, py = cx + dx * radius, cy + dy * radius
        pen.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GLOBE_BLUE)


def masthead(pen):
    """Kicker, date line and double rule across the top of the page."""
    pen.text(
        (PAGE_W // 2, 46), "THE DAY IN ONE IMAGE",
        font=font("sans-bold", 21), fill=SCARLET, anchor="ma",
    )
    pen.text(
        (PAGE_W // 2, 80), "THURSDAY, 19 NOVEMBER 2026",
        font=font("serif-bold", 42), fill=TEXT, anchor="ma",
    )
    pen.line([58, 140, PAGE_W - 58, 140], fill=TEXT, width=3)
    pen.line([58, 147, PAGE_W - 58, 147], fill=TEXT, width=1)


def lead_story(pen):
    """The big story of the day: the first three-way summit in Shenzhen."""
    pen.rectangle([40, 164, PAGE_W - 40, 372], fill=SKY, outline=LINE, width=1)
    pen.text((64, 184), "APEC  |  SHENZHEN",
             font=font("sans-bold", 19), fill=SCARLET)
    pen.text((64, 212), "TRUMP, XI AND PUTIN MEET",
             font=font("serif-bold", 35), fill=TEXT)
    pen.text((64, 256), "IN FIRST THREE-WAY SUMMIT",
             font=font("serif-bold", 35), fill=TEXT)
    standfirst = (
        "The US, Chinese and Russian leaders held their first-ever "
        "three-way talks at the APEC summit in Shenzhen."
    )
    lines = fit_lines(pen, standfirst, "sans", 20, 640)
    put_lines(pen, 64, 306, lines, "sans", 20, SOFT, 26)
    draw_world(pen, 890, 268, 60)


STORIES = [
    {
        "kicker": "JUSTICE  |  THE HAGUE",
        "colour": (178, 34, 24),
        "title": "World court: Myanmar committed genocide",
        "body": (
            "The ICJ ruled 9-6 that Myanmar's forces killed about 10,000 "
            "Rohingya, the first time the court has found a state guilty "
            "of genocide."
        ),
    },
    {
        "kicker": "MARKETS  |  NEW YORK",
        "colour": (30, 80, 214),
        "title": "Anthropic's $81bn IPO is the biggest ever",
        "body": (
            "Priced at $83 a share, the Claude maker's debut raised "
            "$81.3bn; shares opened at $111.50 on the Nasdaq, up 34%."
        ),
    },
    {
        "kicker": "UKRAINE",
        "colour": (14, 116, 108),
        "title": "Ukraine hits Crimean Bridge a third time",
        "body": (
            "The rail section was struck and train traffic halted, in the "
            "third attack on the bridge this week, a Russian official said."
        ),
    },
    {
        "kicker": "MIDDLE EAST",
        "colour": (107, 42, 214),
        "title": "Tankers ablaze as Gulf tensions flare",
        "body": (
            "Three oil tankers caught fire after hitting mines east of the "
            "Strait of Hormuz; Houthi attacks damaged Riyadh's tallest "
            "tower."
        ),
    },
]

BRIEFS = [
    "Israeli tanks push into central Gaza",
    "Bangladesh unrest: 4 killed, home torched",
    "LPG tanker Gas Husky sinks off Bulgaria",
    "Jeffries nominated as House Speaker",
    "Denmark approves Greenland deal, 109-0",
    "IAEA: N. Korea expanding enrichment",
]


def story_card(pen, story, x, y, width, height):
    """One card of the 2x2 grid: kicker bar, headline, short body."""
    pen.rectangle([x, y, x + width, y + height],
                  fill=CARD, outline=LINE, width=1)
    pen.rectangle([x, y, x + width, y + 6], fill=story["colour"])
    pen.text((x + 18, y + 20), story["kicker"],
             font=font("sans-bold", 17), fill=story["colour"])
    title_lines = fit_lines(pen, story["title"], "serif-bold", 25, width - 36)
    next_y = put_lines(pen, x + 18, y + 48, title_lines,
                       "serif-bold", 25, TEXT, 32)
    body_lines = fit_lines(pen, story["body"], "sans", 18, width - 36)
    put_lines(pen, x + 18, next_y + 6, body_lines, "sans", 18, SOFT, 24)


def story_grid(pen):
    """Lay the four story cards out in two rows of two."""
    card_w, card_h, gap = 464, 196, 16
    for index, story in enumerate(STORIES):
        col = index % 2
        row = index // 2
        x = 40 + col * (card_w + gap)
        y = 392 + row * (card_h + gap)
        story_card(pen, story, x, y, card_w, card_h)


def briefs_panel(pen):
    """The navy 'also today' strip with six one-line briefs."""
    pen.rectangle([40, 816, PAGE_W - 40, 948], fill=DARK)
    pen.text((64, 832), "ALSO TODAY",
             font=font("sans-bold", 20), fill=GOLD)
    for index, brief in enumerate(BRIEFS):
        col = index % 2
        row = index // 2
        x = 64 + col * 470
        y = 862 + row * 30
        pen.ellipse([x, y + 7, x + 8, y + 15], fill=GOLD)
        pen.text((x + 18, y), brief, font=font("sans", 18),
                 fill=(240, 240, 240))


def build():
    """Draw the whole front page and save it as entry.png."""
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    pen = ImageDraw.Draw(sheet)
    pen.rectangle([14, 14, PAGE_W - 15, PAGE_H - 15], outline=TEXT, width=3)
    masthead(pen)
    lead_story(pen)
    story_grid(pen)
    briefs_panel(pen)
    pen.text(
        (PAGE_W // 2, 962),
        "Headlines as reported on 19 November 2026  |  "
        "Sources: AA, Reuters, Al Jazeera",
        font=font("sans", 15), fill=FAINT, anchor="ma",
    )
    sheet.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
