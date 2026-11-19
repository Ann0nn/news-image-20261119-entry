# Renders entry.png: a one-page newspaper summary of the world news of
# Thursday 19 November 2026. Run: python3 src/render.py
# Output: entry.png at the repository root, 1024x1024, under 1 MiB.
# Headlines were researched from live news sources on 19 Nov 2026
# (AA, Reuters via Business Times and Jerusalem Post, Al Jazeera, Japan
# Times, Malay Mail, Haaretz): every story below happened or was first
# reported on 19 November 2026.

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (18, 18, 18)
GREY = (90, 90, 90)
NAVY = (15, 42, 74)
RED = (163, 22, 33)
LEAD_BG = (234, 240, 246)
RULE = (180, 180, 175)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
serif_b = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", s)
serif = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", s)
sans_b = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", s)
sans = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", s)


def wrap(draw, text, font, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """Simple line globe: circle, meridians, parallels."""
    c = (70, 110, 160)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=c, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=c, width=3)
    draw.arc([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], 0, 180, fill=c, width=3)
    draw.arc([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], 180, 360, fill=c, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)

    # ---- Masthead ----
    d.text((W // 2, 44), "THE DAY IN ONE IMAGE", font=sans_b(21),
           fill=RED, anchor="ma")
    d.text((W // 2, 78), "THURSDAY, 19 NOVEMBER 2026", font=serif_b(44),
           fill=INK, anchor="ma")
    d.line([60, 140, W - 60, 140], fill=INK, width=3)
    d.line([60, 147, W - 60, 147], fill=INK, width=1)

    # ---- Lead story ----
    d.rectangle([40, 164, W - 40, 372], fill=LEAD_BG, outline=RULE, width=1)
    d.text((64, 184), "APEC  |  SHENZHEN", font=sans_b(19), fill=RED)
    d.text((64, 214), "TRUMP, XI AND PUTIN MEET", font=serif_b(36), fill=INK)
    d.text((64, 258), "IN FIRST THREE-WAY SUMMIT", font=serif_b(36), fill=INK)
    lead = ("The US, Chinese and Russian leaders held their first-ever "
            "three-way talks at the APEC summit in Shenzhen.")
    y = 306
    for line in wrap(d, lead, sans(20), 640):
        d.text((64, y), line, font=sans(20), fill=(40, 40, 40))
        y += 26
    draw_globe(d, 890, 268, 62)

    # ---- Four stories, 2x2 grid ----
    stories = [
        ("JUSTICE  |  THE HAGUE", (180, 35, 24),
         "World court: Myanmar committed genocide",
         "The ICJ ruled 9-6 that Myanmar's forces killed about 10,000 "
         "Rohingya, the first time the court has found a state guilty of "
         "genocide."),
        ("MARKETS  |  NEW YORK", (29, 78, 216),
         "Anthropic's $81bn IPO is the biggest ever",
         "Priced at $83 a share, the Claude maker's debut raised $81.3bn; "
         "shares opened at $111.50 on the Nasdaq, up 34%."),
        ("UKRAINE", (15, 118, 110),
         "Ukraine hits Crimean Bridge a third time",
         "The rail section was struck and train traffic halted, in the "
         "third attack on the bridge this week, a Russian official said."),
        ("MIDDLE EAST", (109, 40, 217),
         "Tankers ablaze as Gulf tensions flare",
         "Three oil tankers caught fire after hitting mines east of the "
         "Strait of Hormuz; Houthi attacks damaged Riyadh's tallest tower."),
    ]
    gx, gy, cw, ch, gap = 40, 392, 464, 196, 16
    for i, (tag, colour, head, body) in enumerate(stories):
        x = gx + (i % 2) * (cw + gap)
        yy = gy + (i // 2) * (ch + gap)
        d.rectangle([x, yy, x + cw, yy + ch], fill=(255, 255, 255),
                    outline=RULE, width=1)
        d.rectangle([x, yy, x + cw, yy + 6], fill=colour)
        d.text((x + 18, yy + 20), tag, font=sans_b(17), fill=colour)
        hy = yy + 48
        for line in wrap(d, head, serif_b(25), cw - 36):
            d.text((x + 18, hy), line, font=serif_b(25), fill=INK)
            hy += 32
        by = hy + 6
        for line in wrap(d, body, sans(18), cw - 36):
            d.text((x + 18, by), line, font=sans(18), fill=(50, 50, 50))
            by += 24

    # ---- Also today ----
    d.rectangle([40, 816, W - 40, 948], fill=NAVY)
    d.text((64, 832), "ALSO TODAY", font=sans_b(20), fill=(255, 205, 60))
    also = [
        "Israeli tanks push into central Gaza",
        "Bangladesh unrest: 4 killed, home torched",
        "LPG tanker Gas Husky sinks off Bulgaria",
        "Jeffries nominated as House Speaker",
        "Denmark approves Greenland deal, 109-0",
        "IAEA: N. Korea expanding enrichment",
    ]
    for i, item in enumerate(also):
        x = 64 + (i % 2) * 470
        y = 862 + (i // 2) * 30
        d.ellipse([x, y + 7, x + 8, y + 15], fill=(255, 205, 60))
        d.text((x + 18, y), item, font=sans(18), fill=(240, 240, 240))

    # ---- Footer ----
    d.text((W // 2, 962), "Headlines as reported on 19 November 2026  |  "
           "Sources: AA, Reuters, Al Jazeera", font=sans(15), fill=GREY,
           anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
