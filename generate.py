#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261121.
Deterministic: fixed text, fixed fonts, no time, no random, no network.
Run: python3 generate.py  -> writes entry.png (1024x1024, <1MiB).
The submitted program (main.py) only copies entry.png to /output.
Headlines verified 2026-11-21 from OneTurn / AP / CBS / NYT / Reuters /
ISW / AFP / UN News listings.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, color, max_w, lh=None):
    lh = lh or int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y

img = Image.new("RGB", (W, H), "#F7F2E6")
d = ImageDraw.Draw(img)

# ---- header ----
d.rectangle([0, 0, W, 118], fill="#10243E")
d.text((28, 22), "WORLD NEWS", font=font(62), fill="white")
d.text((28, 88), "SATURDAY  •  THE DAY IN ONE PICTURE", font=font(20), fill="#F2C14E")
d.text((700, 30), "21 NOV", font=font(52), fill="white")
d.text((700, 88), "2026", font=font(28), fill="#F2C14E")

# ---- main story: Russia's barrage on Ukraine ----
d.rounded_rectangle([24, 138, 624, 560], radius=14, fill="white", outline="#10243E", width=3)
d.text((44, 156), "KYIV  •  CONFLICT", font=font(20), fill="#B03A2E")
text_block(d, 44, 186, "RUSSIA'S BIGGEST NOVEMBER BARRAGE", font(34), "#10243E", 540)
text_block(d, 44, 262, "400+ drones and 110+ missiles hit Ukraine overnight; at least 8 killed in Kyiv.", font(24, False), "#222222", 540)
# blast graphic: dark sky, red impact bursts, three bridges
d.rectangle([44, 352, 604, 518], fill="#10243E")
for cx, cy, r in [(140, 420, 26), (300, 392, 34), (470, 430, 24), (540, 384, 16)]:
    for k in range(8):
        import math
        a = k * math.pi / 4
        d.line([cx, cy, cx + int(r * 1.6 * math.cos(a)), cy + int(r * 1.6 * math.sin(a))], fill="#F2C14E", width=3)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2], fill="#B03A2E")
d.line([70, 488, 200, 488, 260, 462, 340, 488, 580, 488], fill="#9FC3E8", width=4)
d.text((44, 528), "3 KYIV BRIDGES HIT  •  MISSILES LAND IN POLAND", font=font(18), fill="#10243E")

# ---- right column: markets + climate ----
d.rounded_rectangle([644, 138, 1000, 340], radius=14, fill="#10243E")
d.text((664, 156), "NEW YORK  •  MARKETS", font=font(19), fill="#F2C14E")
text_block(d, 664, 186, "AI sell-off: S&P 500 -3.7% into correction; Nasdaq -5.3%.", font(24), "white", 316)
d.text((664, 296), "NVIDIA -14% ON SEC PROBE", font=font(19), fill="#9FC3E8")
d.rounded_rectangle([644, 360, 1000, 560], radius=14, fill="white", outline="#10243E", width=3)
d.text((664, 378), "ANTALYA  •  CLIMATE", font=font(19), fill="#B03A2E")
text_block(d, 664, 406, "COP31 runs past deadline; draft drops fossil-fuel language.", font(23), "#10243E", 316)
# falling chart
pts = [(670, 500), (730, 510), (790, 506), (850, 520), (910, 532), (975, 545)]
d.line(pts, fill="#B03A2E", width=5, joint="curve")
for x, y in pts:
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill="#B03A2E")

# ---- bottom row: three stories ----
panels = [
    ("WASHINGTON  •  POLITICS", "Trump weighs new strikes on Iran as Israel presses for action.", "#B03A2E"),
    ("THE HAGUE  •  JUSTICE", "Myanmar rejects World Court genocide ruling; Beijing backs it.", "#B03A2E"),
    ("HEALTH  •  SCIENCE", "Pancreatic cancer pill makes tumours undetectable in 1 in 12 patients.", "#B03A2E"),
]
for i, (kicker, body, kc) in enumerate(panels):
    x0 = 24 + i * 330
    d.rounded_rectangle([x0, 580, x0 + 310, 820], radius=14, fill="white", outline="#10243E", width=3)
    d.text((x0 + 18, 600), kicker, font=font(17), fill=kc)
    text_block(d, x0 + 18, 634, body, font(23), "#10243E", 274)
    d.rectangle([x0 + 18, 780, x0 + 292, 786], fill="#F2C14E")

# ---- footer strip ----
d.rectangle([0, 860, W, 1024], fill="#10243E")
text_block(d, 28, 884, "Also: Gaza strikes kill 6  •  Ukraine's 'Bear Trap' frees 200 sq km  •  Nikkei -5.1%, Kospi -5.2%  •  Saudi coalition warns Hodeidah to evacuate", font(22), "white", 968)
d.text((28, 972), "21 NOVEMBER 2026  •  SOURCES: AP / CBS / NYT / REUTERS / ISW / AFP  •  ONE IMAGE, ONE DAY", font=font(18), fill="#F2C14E")

img.save("entry.png", "PNG", optimize=True)
print("wrote entry.png", img.size)
