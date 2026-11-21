"""Render the 21 November 2026 world-news front page as a PNG.

The page is a newspaper front page on warm newsprint: a masthead,
one lead story, five more stories in a two-column grid, an "in brief"
box, and a source line. Every mark on the page is drawn in code with
Pillow. There are no photographs, no network calls, no clock reads
and no random numbers, so the output is byte-identical on every run.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 46
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (246, 241, 231)
INK = (26, 26, 26)
SOFT_INK = (58, 54, 46)
RED = (176, 32, 28)
GREY = (104, 98, 84)
HAIR = (198, 190, 174)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

LEAD = {
    "kicker": "CONFLICT — UKRAINE AND POLAND",
    "headline": "Russia's biggest November barrage hits Ukraine — and spills into Poland",
    "deck": (
        "Overnight on 19–20 November, 404 drones and 111 missiles struck across "
        "Ukraine, killing at least eight people in Kyiv and damaging three bridges. "
        "Two missiles and a drone came down in Poland."
    ),
}

STATS = [
    ("404", "drones fired"),
    ("111", "missiles fired"),
    ("8", "killed in Kyiv"),
]

STORIES = [
    {
        "kicker": "JUSTICE — THE HAGUE",
        "headline": "World Court: Myanmar guilty of Rohingya genocide",
        "body": "The 9–6 ruling, a first for the court, orders reparations and a safe, voluntary return.",
    },
    {
        "kicker": "MARKETS — NEW YORK",
        "headline": "AI sell-off drags the S&P 500 into correction",
        "body": "US stocks fell 3.7% on Friday, days after Anthropic's debut valued it at $2 trillion.",
    },
    {
        "kicker": "CLIMATE — ANTALYA",
        "headline": "COP31 overruns as fossil fuels fall out of the deal",
        "body": "The draft drops the pledge to move away from coal, oil and gas, and concedes 1.5°C will be overshot.",
    },
    {
        "kicker": "DIPLOMACY — SHENZHEN",
        "headline": "Trump, Xi and Putin sign a four-point peace declaration",
        "body": "The first three-way meeting of the three leaders says nothing about Ukraine.",
    },
    {
        "kicker": "HEALTH — LONDON",
        "headline": "Trial pill clears pancreatic tumours in one in 12 patients",
        "body": "Daraxonrasib made the cancer undetectable on scans in the trial.",
    },
]

BRIEFS = [
    "Kryvyi Rih: a Russian missile strike kills 2 and wounds 60.",
    "Iran says it downed a US MQ-9 drone over the Strait of Hormuz.",
]

SOURCES = (
    "Sources: Associated Press · The New York Times · One Turn · Majik Brief "
    "— all facts verified 21 November 2026"
)
CREDIT = "Drawn entirely in code · Python + Pillow · No photographs"


def _font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def _wrap(draw, text, font, width):
    """Split text into lines that fit inside width."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _fit(draw, text, font, width, limit):
    """Wrap text, cutting it to at most limit lines with an ellipsis."""
    lines = _wrap(draw, text, font, width)
    if len(lines) <= limit:
        return lines
    lines = lines[:limit]
    while lines and draw.textlength(lines[-1] + "…", font=font) > width:
        lines[-1] = lines[-1][:-1]
    lines[-1] = lines[-1].rstrip() + "…"
    return lines


def _masthead(draw):
    title = _font("DejaVuSerif-Bold.ttf", 52)
    draw.text((PAGE_W / 2, 42), "THE WORLD IN ONE IMAGE",
              font=title, fill=INK, anchor="ma")
    small = _font("DejaVuSans.ttf", 18)
    draw.text((MARGIN, 114), "SATURDAY, 21 NOVEMBER 2026",
              font=small, fill=GREY, anchor="la")
    draw.text((PAGE_W - MARGIN, 114), "SIX STORIES · ONE PAGE",
              font=small, fill=GREY, anchor="ra")
    draw.line([(MARGIN, 144), (PAGE_W - MARGIN, 144)], fill=INK, width=3)
    draw.line([(MARGIN, 150), (PAGE_W - MARGIN, 150)], fill=INK, width=1)


def _lead(draw):
    kicker = _font("DejaVuSans-Bold.ttf", 19)
    draw.text((MARGIN, 170), LEAD["kicker"], font=kicker, fill=RED, anchor="la")
    head = _font("DejaVuSerif-Bold.ttf", 42)
    lines = _fit(draw, LEAD["headline"], head, CONTENT_W, 2)
    y = 198
    for line in lines:
        draw.text((MARGIN, y), line, font=head, fill=INK, anchor="la")
        y += 50
    deck = _font("DejaVuSans.ttf", 21)
    for line in _fit(draw, LEAD["deck"], deck, CONTENT_W, 3):
        draw.text((MARGIN, y + 6), line, font=deck, fill=SOFT_INK, anchor="la")
        y += 29
    return y + 6


def _stats(draw, y):
    number = _font("DejaVuSerif-Bold.ttf", 42)
    label = _font("DejaVuSans.ttf", 16)
    span = CONTENT_W / 3
    for i, (value, text) in enumerate(STATS):
        cx = MARGIN + span * (i + 0.5)
        draw.text((cx, y), value, font=number, fill=RED, anchor="ma")
        draw.text((cx, y + 50), text, font=label, fill=GREY, anchor="ma")
        if i:
            x = MARGIN + span * i
            draw.line([(x, y + 4), (x, y + 66)], fill=HAIR, width=1)
    return y + 72


def _card(draw, x, y, w, story):
    draw.line([(x, y), (x + w, y)], fill=INK, width=2)
    kicker = _font("DejaVuSans-Bold.ttf", 16)
    head = _font("DejaVuSerif-Bold.ttf", 24)
    body = _font("DejaVuSans.ttf", 17)
    draw.text((x, y + 10), story["kicker"], font=kicker, fill=RED, anchor="la")
    ty = y + 34
    for line in _fit(draw, story["headline"], head, w, 2):
        draw.text((x, ty), line, font=head, fill=INK, anchor="la")
        ty += 29
    for line in _fit(draw, story["body"], body, w, 2):
        draw.text((x, ty + 4), line, font=body, fill=SOFT_INK, anchor="la")
        ty += 22


def _briefs(draw, x, y, w):
    draw.line([(x, y), (x + w, y)], fill=INK, width=2)
    kicker = _font("DejaVuSans-Bold.ttf", 16)
    body = _font("DejaVuSans.ttf", 17)
    draw.text((x, y + 10), "IN BRIEF", font=kicker, fill=RED, anchor="la")
    ty = y + 34
    for item in BRIEFS:
        for line in _fit(draw, "•  " + item, body, w, 2):
            draw.text((x, ty), line, font=body, fill=SOFT_INK, anchor="la")
            ty += 22
        ty += 4


def render():
    """Build the front page and return it as a Pillow image."""
    image = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle([24, 24, PAGE_W - 24, PAGE_H - 24], outline=INK, width=2)
    _masthead(draw)
    y = _lead(draw)
    y = _stats(draw, y + 8)
    draw.line([(MARGIN, y + 10), (PAGE_W - MARGIN, y + 10)], fill=HAIR, width=1)
    grid_y = y + 24
    col_w = (CONTENT_W - 28) // 2
    row_h, row_gap = 128, 12
    cells = [
        (MARGIN, grid_y),
        (MARGIN + col_w + 28, grid_y),
        (MARGIN, grid_y + row_h + row_gap),
        (MARGIN + col_w + 28, grid_y + row_h + row_gap),
        (MARGIN, grid_y + 2 * (row_h + row_gap)),
        (MARGIN + col_w + 28, grid_y + 2 * (row_h + row_gap)),
    ]
    for (cx, cy), story in zip(cells[:5], STORIES):
        _card(draw, cx, cy, col_w, story)
    _briefs(draw, cells[5][0], cells[5][1], col_w)
    foot_y = grid_y + 3 * row_h + 2 * row_gap + 14
    draw.line([(MARGIN, foot_y), (PAGE_W - MARGIN, foot_y)], fill=INK, width=1)
    small = _font("DejaVuSans.ttf", 15)
    draw.text((PAGE_W / 2, foot_y + 10), SOURCES,
              font=small, fill=GREY, anchor="ma")
    draw.text((PAGE_W / 2, foot_y + 32), CREDIT,
              font=small, fill=GREY, anchor="ma")
    return image
