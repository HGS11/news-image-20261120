"""Deterministic broadsheet front page generator for 20 November 2026."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

BG = "#f7f2e7"
PANEL_BG = "#efe8d8"
INK = "#141414"
MUTED = "#4b463d"
RULE = "#8c8270"
DARK_RULE = "#2b2620"
RED = "#b91c1c"
NAVY = "#1e3a8a"
TEAL = "#0f766e"
GREEN = "#15803d"
OCHRE = "#b45309"
SLATE = "#374151"

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_size(draw, txt, fnt):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]


def draw_text_fit(draw, xy, txt, fnt, fill, max_w=None, anchor="lt"):
    if max_w is not None:
        tw, _ = text_size(draw, txt, fnt)
        if tw > max_w:
            raise ValueError(f"Text overflow ({tw} > {max_w}): {txt}")
    draw.text(xy, txt, font=fnt, fill=fill, anchor=anchor)


def wrap_lines(draw, txt, fnt, max_w):
    words = txt.split()
    lines, cur = [], ""
    for word in words:
        cand = (cur + " " + word).strip()
        tw, _ = text_size(draw, cand, fnt)
        if tw <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lead_1_art(draw, x0, y0, x1, y1):
    # Summit room with 3 flags and 3 presidents at one table
    draw.rectangle([x0, y0, x1, y1], fill="#dce3ea", outline=DARK_RULE, width=1)
    draw.rectangle([x0 + 1, y0 + 1, x1 - 1, y0 + 22], fill="#1e3a8a")
    draw.text(((x0 + x1) // 2, y0 + 11), "APEC SHENZHEN", font=font(F_SANS_B, 10), fill="#f7f2e7", anchor="mm")

    cx_list = [x0 + 68, (x0 + x1) // 2, x1 - 68]
    # US flag
    fx, fy = cx_list[0] - 18, y0 + 28
    draw.line([fx - 2, fy, fx - 2, y0 + 78], fill="#4b5563", width=2)
    draw.rectangle([fx, fy, fx + 34, fy + 20], fill="#ffffff", outline="#374151", width=1)
    for i in range(0, 20, 4):
        draw.rectangle([fx + 1, fy + i, fx + 33, fy + i + 2], fill="#b91c1c")
    draw.rectangle([fx + 1, fy + 1, fx + 15, fy + 11], fill="#1e3a8a")
    # China flag
    fx, fy = cx_list[1] - 17, y0 + 28
    draw.line([fx - 2, fy, fx - 2, y0 + 78], fill="#4b5563", width=2)
    draw.rectangle([fx, fy, fx + 34, fy + 20], fill="#dc2626", outline="#374151", width=1)
    draw.ellipse([fx + 4, fy + 4, fx + 10, fy + 10], fill="#facc15")
    # Russia flag
    fx, fy = cx_list[2] - 16, y0 + 28
    draw.line([fx - 2, fy, fx - 2, y0 + 78], fill="#4b5563", width=2)
    draw.rectangle([fx, fy, fx + 34, fy + 7], fill="#ffffff")
    draw.rectangle([fx, fy + 7, fx + 34, fy + 14], fill="#1d4ed8")
    draw.rectangle([fx, fy + 14, fx + 34, fy + 20], fill="#dc2626")
    draw.rectangle([fx, fy, fx + 34, fy + 20], outline="#374151", width=1)

    leaders = [
        (cx_list[0], "#f3cfa4", "#eab308", "#1e293b", "#dc2626"),
        (cx_list[1], "#edd0aa", "#1f2937", "#111827", "#b91c1c"),
        (cx_list[2], "#f4d6b8", "#d4b483", "#1f2937", "#2563eb"),
    ]
    for cx, skin, hair, suit, tie in leaders:
        draw.polygon([(cx - 22, y0 + 82), (cx + 22, y0 + 82), (cx + 16, y0 + 62), (cx - 16, y0 + 62)], fill=suit)
        draw.polygon([(cx - 5, y0 + 62), (cx + 5, y0 + 62), (cx, y0 + 75)], fill="#ffffff")
        draw.polygon([(cx - 2, y0 + 65), (cx + 2, y0 + 65), (cx, y0 + 80)], fill=tie)
        draw.ellipse([cx - 10, y0 + 42, cx + 10, y0 + 62], fill=skin, outline="#374151", width=1)
        draw.chord([cx - 10, y0 + 40, cx + 10, y0 + 52], 180, 360, fill=hair)

    draw.rectangle([x0 + 18, y0 + 80, x1 - 18, y1 - 10], fill="#7c4a2d", outline="#3e2414", width=1)
    draw.rectangle([x0 + 18, y0 + 80, x1 - 18, y0 + 86], fill="#9a5e3a")
    for cx in cx_list:
        draw.rectangle([cx - 9, y0 + 88, cx + 9, y0 + 95], fill="#f7f2e7")
        draw.line([cx + 12, y0 + 84, cx + 12, y0 + 76], fill="#111827", width=2)


def draw_lead_2_art(draw, x0, y0, x1, y1):
    # Dark navy candlestick chart rising steeply with green arrow
    draw.rectangle([x0, y0, x1, y1], fill="#0f172a", outline=DARK_RULE, width=1)
    for gx in range(x0 + 36, x1, 44):
        draw.line([gx, y0 + 8, gx, y1 - 8], fill="#1e293b", width=1)
    for gy in range(y0 + 22, y1 - 8, 22):
        draw.line([x0 + 8, gy, x1 - 8, gy], fill="#1e293b", width=1)

    candles = [
        (32, 92, 82, "#ef4444"),
        (56, 86, 74, "#22c55e"),
        (80, 78, 84, "#ef4444"),
        (104, 80, 64, "#22c55e"),
        (128, 66, 54, "#22c55e"),
        (152, 58, 62, "#ef4444"),
        (176, 56, 38, "#22c55e"),
        (200, 42, 26, "#22c55e"),
        (224, 30, 18, "#22c55e"),
    ]
    for dx, o, c, col in candles:
        cx = x0 + dx
        top, bot = y0 + min(o, c), y0 + max(o, c)
        draw.line([cx, top - 7, cx, bot + 7], fill=col, width=2)
        draw.rectangle([cx - 7, top, cx + 7, bot], fill=col)

    draw.line([x0 + 26, y0 + 96, x0 + 268, y0 + 24], fill="#4ade80", width=4)
    draw.polygon([(x0 + 276, y0 + 21), (x0 + 256, y0 + 20), (x0 + 266, y0 + 36)], fill="#4ade80")
    draw.rectangle([x0 + 14, y0 + 10, x0 + 124, y0 + 34], fill="#1e293b", outline="#4ade80", width=1)
    draw.text((x0 + 69, y0 + 22), "$81.3bn · +17%", font=font(F_SANS_B, 11), fill="#4ade80", anchor="mm")


def draw_lead_3_art(draw, x0, y0, x1, y1):
    # World Court neoclassical facade with columns and golden scales
    draw.rectangle([x0, y0, x1, y1], fill="#d9e6f2", outline=DARK_RULE, width=1)
    draw.rectangle([x0 + 1, y1 - 20, x1 - 1, y1 - 1], fill="#9ca3af")
    cx = (x0 + x1) // 2

    draw.rectangle([cx - 108, y0 + 44, cx + 108, y1 - 20], fill="#ede4d3", outline="#57534e", width=1)
    draw.polygon([(cx - 118, y0 + 44), (cx + 118, y0 + 44), (cx, y0 + 16)], fill="#b91c1c", outline="#450a0a")
    draw.polygon([(cx - 98, y0 + 42), (cx + 98, y0 + 42), (cx, y0 + 22)], fill="#e7dcc8")

    for off in [-84, -52, -20, 20, 52, 84]:
        draw.rectangle([cx + off - 6, y0 + 46, cx + off + 6, y1 - 24], fill="#f7f2e7", outline="#78716c", width=1)
    draw.rectangle([cx - 116, y1 - 24, cx + 116, y1 - 16], fill="#d6cfc2", outline="#57534e", width=1)

    draw.line([cx, y0 + 50, cx, y1 - 14], fill="#b45309", width=3)
    draw.rectangle([cx - 18, y1 - 16, cx + 18, y1 - 10], fill="#b45309")
    draw.line([cx - 34, y0 + 58, cx + 34, y0 + 58], fill="#d97706", width=3)
    for sx in (cx - 32, cx + 32):
        draw.line([sx, y0 + 58, sx - 10, y0 + 78], fill="#92400e", width=1)
        draw.line([sx, y0 + 58, sx + 10, y0 + 78], fill="#92400e", width=1)
        draw.chord([sx - 12, y0 + 72, sx + 12, y0 + 84], 0, 180, fill="#f59e0b", outline="#92400e")


def draw_grid_art(draw, idx, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if idx == 4:
        draw.rectangle([x0, y0, x1, y1], fill="#dbeafe", outline=DARK_RULE, width=1)
        draw.rectangle([x0 + 1, y1 - 14, x1 - 1, y1 - 1], fill="#fef08a")
        draw.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 14], fill="#2563eb")
        draw.polygon([(cx - 48, cy + 4), (cx - 8, cy - 6), (cx + 8, cy - 6), (cx + 48, cy + 4), (cx + 8, cy + 2), (cx - 8, cy + 2)], fill="#111827")
        draw.ellipse([cx - 14, cy - 10, cx + 14, cy + 4], fill="#1f2937")
        draw.line([cx - 38, cy - 4, cx - 22, cy - 4], fill="#facc15", width=2)
        draw.line([cx + 22, cy - 4, cx + 38, cy - 4], fill="#facc15", width=2)
    elif idx == 5:
        draw.rectangle([x0, y0, x1, y1], fill="#fef3c7", outline=DARK_RULE, width=1)
        draw.polygon([(cx - 12, y1 - 2), (cx - 8, y0 + 6), (cx + 8, y0 + 6), (cx + 12, y1 - 2)], fill="#334155")
        draw.ellipse([cx - 5, y0 + 9, cx + 5, y0 + 21], fill="#fef3c7")
        draw.polygon([(cx + 8, y0 + 22), (cx + 24, y0 + 12), (cx + 18, y0 + 24), (cx + 32, y0 + 26), (cx + 18, y0 + 32), (cx + 24, y0 + 40), (cx + 8, y0 + 30)], fill="#dc2626")
    elif idx == 6:
        draw.rectangle([x0, y0, x1, y1], fill="#e0f2fe", outline=DARK_RULE, width=1)
        draw.ellipse([cx - 30, cy - 18, cx + 6, cy + 18], fill="#0284c7", outline=DARK_RULE, width=1)
        draw.polygon([(cx - 22, cy - 10), (cx - 10, cy - 12), (cx - 4, cy + 2), (cx - 16, cy + 10)], fill="#16a34a")
        draw.rectangle([cx + 18, y0 + 7, cx + 26, y1 - 14], fill="#ffffff", outline=DARK_RULE, width=1)
        draw.ellipse([cx + 15, y1 - 19, cx + 29, y1 - 5], fill="#dc2626", outline=DARK_RULE, width=1)
        draw.rectangle([cx + 20, y0 + 14, cx + 24, y1 - 10], fill="#dc2626")
    elif idx == 7:
        draw.rectangle([x0, y0, x1, y1], fill="#e2e8f0", outline=DARK_RULE, width=1)
        draw.rectangle([cx - 26, y0 + 8, cx + 26, y1 - 6], fill="#d6b88d", outline="#78350f", width=1)
        draw.rectangle([cx - 10, y0 + 16, cx + 10, y1 - 14], fill="#ffffff")
        draw.rectangle([cx - 3, y0 + 13, cx + 3, y1 - 11], fill="#dc2626")
        draw.rectangle([cx - 10, cy - 2, cx + 10, cy + 4], fill="#dc2626")
    elif idx == 8:
        draw.rectangle([x0, y0, x1, y1], fill="#eff6ff", outline=DARK_RULE, width=1)
        draw.rectangle([cx - 24, cy - 2, cx + 24, y1 - 5], fill="#1d4ed8", outline=DARK_RULE, width=1)
        draw.rectangle([cx - 14, cy + 2, cx + 14, cy + 6], fill="#0f172a")
        draw.polygon([(cx - 10, y0 + 6), (cx + 10, y0 + 6), (cx + 10, cy + 4), (cx - 10, cy + 4)], fill="#ffffff", outline=DARK_RULE)
        draw.line([cx - 5, y0 + 14, cx - 1, y0 + 18], fill="#15803d", width=2)
        draw.line([cx - 1, y0 + 18, cx + 6, y0 + 10], fill="#15803d", width=2)
    elif idx == 9:
        draw.rectangle([x0, y0, x1, y1], fill="#1e293b", outline=DARK_RULE, width=1)
        draw.rectangle([cx - 44, y1 - 15, cx + 44, y1 - 3], fill="#e2e8f0")
        draw.rectangle([cx - 22, cy - 2, cx + 22, y1 - 15], fill="#f8fafc")
        draw.chord([cx - 18, y0 + 10, cx + 18, cy + 6], 180, 360, fill="#f1f5f9")
        draw.line([cx, y0 + 4, cx, y0 + 12], fill="#f8fafc", width=2)
    elif idx == 10:
        draw.rectangle([x0, y0, x1, y1], fill="#18181b", outline=DARK_RULE, width=1)
        pts = [(x0 + 16, y0 + 10), (x0 + 52, y0 + 18), (x0 + 78, y0 + 14), (x0 + 116, y0 + 32), (x0 + 142, y0 + 28), (x1 - 20, y1 - 10)]
        draw.line(pts, fill="#ef4444", width=3)
        draw.polygon([(x1 - 16, y1 - 7), (x1 - 28, y1 - 9), (x1 - 20, y1 - 18)], fill="#ef4444")
    elif idx == 11:
        draw.rectangle([x0, y0, x1, y1], fill="#fde68a", outline=DARK_RULE, width=1)
        for px in range(x0 + 24, x1 - 20, 26):
            draw.ellipse([px - 5, cy - 2, px + 5, cy + 8], fill="#1f2937")
            draw.rectangle([px - 6, cy + 8, px + 6, y1 - 2], fill="#374151")
            draw.line([px + 7, y0 + 18, px + 7, y1 - 4], fill="#78350f", width=2)
            draw.rectangle([px - 2, y0 + 6, px + 16, y0 + 18], fill="#ffffff", outline="#b91c1c", width=1)
    elif idx == 12:
        draw.rectangle([x0, y0, x1, y1], fill="#dbeafe", outline=DARK_RULE, width=1)
        draw.rectangle([cx + 18, y0 + 8, cx + 48, y0 + 26], fill="#1d4ed8")
        draw.rectangle([cx + 18, y0 + 14, cx + 48, y0 + 20], fill="#ffffff")
        draw.line([cx + 18, y0 + 8, cx + 18, y1 - 4], fill="#475569", width=2)
        draw.polygon([(cx - 18, cy - 4), (cx + 12, cy - 4), (cx + 8, y1 - 4), (cx - 14, y1 - 4)], fill="#7c4a2d", outline="#3e2414")
        draw.ellipse([cx - 6, y0 + 12, cx + 2, y0 + 20], fill="#111827")
    elif idx == 13:
        draw.rectangle([x0, y0, x1, y1], fill="#bae6fd", outline=DARK_RULE, width=1)
        draw.polygon([(cx - 32, cy + 4), (cx + 28, cy - 6), (cx + 18, cy + 12), (cx - 22, cy + 14)], fill="#78350f", outline="#451a03")
        draw.rectangle([x0 + 1, cy + 8, x1 - 1, y1 - 1], fill="#0284c7")
        for wx in range(x0 + 8, x1 - 12, 24):
            draw.arc([wx, cy + 4, wx + 22, cy + 14], 180, 360, fill="#e0f2fe", width=2)


def draw_world_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill="#d8e8f0", outline=DARK_RULE, width=1)
    w = x1 - x0
    h = y1 - y0

    def pt(nx, ny):
        return (int(x0 + nx * w), int(y0 + ny * h))

    land = "#e2d2b5"
    coast = "#9e8e74"
    draw.polygon([pt(0.05, 0.14), pt(0.32, 0.12), pt(0.34, 0.28), pt(0.24, 0.42), pt(0.18, 0.48), pt(0.10, 0.36)], fill=land, outline=coast)
    draw.polygon([pt(0.22, 0.50), pt(0.35, 0.54), pt(0.34, 0.72), pt(0.26, 0.90), pt(0.21, 0.74)], fill=land, outline=coast)
    draw.polygon([pt(0.44, 0.15), pt(0.60, 0.12), pt(0.62, 0.32), pt(0.45, 0.34), pt(0.42, 0.24)], fill=land, outline=coast)
    draw.polygon([pt(0.43, 0.36), pt(0.58, 0.36), pt(0.63, 0.54), pt(0.54, 0.80), pt(0.46, 0.62), pt(0.40, 0.46)], fill=land, outline=coast)
    draw.polygon([pt(0.59, 0.12), pt(0.92, 0.14), pt(0.95, 0.38), pt(0.84, 0.54), pt(0.68, 0.54), pt(0.58, 0.36)], fill=land, outline=coast)
    draw.polygon([pt(0.79, 0.64), pt(0.93, 0.66), pt(0.91, 0.82), pt(0.78, 0.80)], fill=land, outline=coast)

    dots = [
        (1, 0.83, 0.41),
        (2, 0.27, 0.25),
        (3, 0.46, 0.21),
        (4, 0.55, 0.23),
        (5, 0.64, 0.47),
        (6, 0.57, 0.32),
        (7, 0.54, 0.40),
        (8, 0.61, 0.39),
        (9, 0.22, 0.32),
        (10, 0.88, 0.45),
        (11, 0.94, 0.31),
        (12, 0.18, 0.46),
        (13, 0.41, 0.48),
    ]
    f_dot = font(F_SANS_B, 8)
    r = 6
    for num, nx, ny in dots:
        dx, dy = pt(nx, ny)
        draw.ellipse([dx - r, dy - r, dx + r, dy + r], fill=RED, outline="#ffffff", width=1)
        draw.text((dx, dy), str(num), font=f_dot, fill="#ffffff", anchor="mm")


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Outer double newspaper frame
    draw.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)
    draw.rectangle([12, 12, W - 13, H - 13], outline=RULE, width=1)

    x_left, x_right = 18, 1006
    usable_w = x_right - x_left

    # 1. Masthead band (y 12-48)
    f_mast = font(F_SERIF_B, 20)
    draw_text_fit(draw, (x_left + 2, 18), "THE WORLD IN ONE PAGE", f_mast, RED, max_w=340)
    draw_text_fit(
        draw,
        (x_right - 2, 18),
        "30 STORIES · EVERY CONTINENT · ONE DAY",
        f_mast,
        RED,
        max_w=560,
        anchor="rt",
    )
    draw.line([x_left, 45, x_right, 45], fill=DARK_RULE, width=2)
    draw.line([x_left, 48, x_right, 48], fill=RULE, width=1)

    # 2. Date headline (y 48-118)
    f_date = font(F_SERIF_B, 62)
    p1 = "Friday 20 November "
    p2 = "2026"
    w1, _ = text_size(draw, p1, f_date)
    w2, _ = text_size(draw, p2, f_date)
    dx_start = (W - (w1 + w2)) // 2
    draw.text((dx_start, 51), p1, font=f_date, fill=INK)
    draw.text((dx_start + w1, 51), p2, font=f_date, fill=RED)
    draw.line([x_left, 116, x_right, 116], fill=RULE, width=1)

    # 3. Standfirst (y 118-142)
    f_stand = font(F_SERIF, 19)
    standfirst = "Trump, Putin & Xi share table · World Court rules Myanmar genocide · Anthropic record IPO"
    draw_text_fit(draw, (W // 2, 129), standfirst, f_stand, RED, max_w=usable_w, anchor="mm")

    # 4. Region bar (y 142-166)
    regions = [
        ("ASIA-PACIFIC 6", 186, RED),
        ("MIDDLE EAST 3", 174, OCHRE),
        ("EUROPE 4", 152, NAVY),
        ("AFRICA 2", 134, GREEN),
        ("AMERICAS 11", 206, TEAL),
        ("GLOBAL 4", 136, SLATE),
    ]
    f_reg = font(F_SANS_B, 13)
    rx = x_left
    for label, seg_w, col in regions:
        draw.rectangle([rx, 143, rx + seg_w - 1, 165], fill=col)
        draw_text_fit(draw, (rx + seg_w // 2, 154), label, f_reg, "#ffffff", max_w=seg_w - 8, anchor="mm")
        rx += seg_w

    # 5. Figures strip (y 166-212)
    draw.rectangle([x_left, 167, x_right, 211], fill=PANEL_BG)
    figs = [
        ("3", "presidents at one table", 140, RED),
        ("9-6", "World Court genocide vote", 158, INK),
        ("$81.3bn", "Anthropic IPO, largest ever", 162, RED),
        ("17%", "Anthropic first-day rise", 138, INK),
        ("£260m", "UK drone package for Ukraine", 178, RED),
        ("$12bn", "Venezuelan oil revenue in US report", 212, INK),
    ]
    f_fignum = font(F_SANS_B, 26)
    f_figcap = font(F_SANS, 11)
    fx = x_left
    for idx, (num, cap, cw, col) in enumerate(figs):
        cx = fx + cw // 2
        draw_text_fit(draw, (cx, 168), num, f_fignum, col, max_w=cw - 6, anchor="mt")
        draw_text_fit(draw, (cx, 196), cap, f_figcap, MUTED, max_w=cw - 4, anchor="mt")
        if idx < len(figs) - 1:
            draw.line([fx + cw, 171, fx + cw, 207], fill=RULE, width=1)
        fx += cw
    draw.line([x_left, 212, x_right, 212], fill=DARK_RULE, width=2)

    # 6. Three large lead stories (y 212-478)
    leads = [
        (
            "1 SHENZHEN · SUMMIT",
            "Trump, Putin and Xi hold first three-way summit",
            "90 mins at APEC Shenzhen; 4-point peace pact on nuclear, energy, UN & law.",
            "Source: AnewZ",
            draw_lead_1_art,
        ),
        (
            "2 NEW YORK · MARKETS",
            "Anthropic shares jump 17% on Nasdaq debut",
            "Record $81.3bn IPO at $83/share; Asian stocks drop on AI-bubble fears.",
            "Source: NPR",
            draw_lead_2_art,
        ),
        (
            "3 THE HAGUE · JUSTICE",
            "World Court: Myanmar committed genocide",
            "9-6 vote after seven years of hearings; 730,000 Rohingya fled in 2017.",
            "Source: NYT",
            draw_lead_3_art,
        ),
    ]
    lead_w = 318
    lead_xs = [x_left, x_left + 335, x_left + 670]
    f_lkick = font(F_SANS_B, 11)
    f_lhead = font(F_SERIF_B, 21)
    f_lbody = font(F_SANS, 13)
    f_lsrc = font(F_SANS, 10)

    for i, (kick, head, body, src, art_fn) in enumerate(leads):
        lx = lead_xs[i]
        art_fn(draw, lx, 217, lx + lead_w, 333)
        draw_text_fit(draw, (lx, 339), kick, f_lkick, RED, max_w=lead_w)
        h_lines = wrap_lines(draw, head, f_lhead, lead_w)[:2]
        for li, line in enumerate(h_lines):
            draw.text((lx, 355 + li * 25), line, font=f_lhead, fill=INK)
        b_lines = wrap_lines(draw, body, f_lbody, lead_w)[:2]
        for bi, line in enumerate(b_lines):
            draw.text((lx, 412 + bi * 17), line, font=f_lbody, fill=MUTED)
        draw_text_fit(draw, (lx, 456), src, f_lsrc, MUTED, max_w=lead_w)
        if i < 2:
            gx = lx + lead_w + 8
            draw.line([gx, 218, gx, 472], fill=RULE, width=1)

    draw.line([x_left, 477, x_right, 477], fill=DARK_RULE, width=2)

    # 7. Two rows of smaller stories (y 478-736)
    grid_stories = [
        (4, "KYIV · WAR", NAVY, "UK pledges 1,000 Ukraine drones", "£260m long-range drone aid."),
        (5, "RIYADH · WAR", OCHRE, "Houthis strike Saudi skyscraper", "4 targets hit; tallest tower hit."),
        (6, "ANTALYA · CLIMATE", OCHRE, "COP31 finance fight goes on", "Africa seeks tripled finance."),
        (7, "GAZA · AID", OCHRE, "Four nations demand Gaza aid", "4 nations urge Gaza aid."),
        (8, "JERUSALEM · POLITICS", OCHRE, "Eisenkot tapped to form government", "Picked ahead of Netanyahu."),
        (9, "WASHINGTON · POLITICS", TEAL, "Senate rejects Iran war bid", "51-48 vote; delayed to 2027."),
        (10, "TAIPEI · MARKETS", RED, "Taiwan stocks plunge 2,200 points", "Down 7,000 pts in a week."),
        (11, "TOKYO · PROTEST", RED, "13,000 march in Tokyo", "Crowds hit Takaichi policies."),
        (12, "SAN SALVADOR · POLITICS", TEAL, "Bukele seeks third term", "Set to file for third term."),
        (13, "DAKAR · MIGRATION", GREEN, "Senegal boat capsizes, four dead", "Boat sinks in migration surge."),
    ]
    cell_w = 188
    col_xs = [x_left + c * 200 for c in range(5)]
    f_gkick = font(F_SANS_B, 11)
    f_ghead = font(F_SANS_B, 15)
    f_gbody = font(F_SANS, 12)

    for idx, (num, place_topic, kcol, head, stand) in enumerate(grid_stories):
        row = idx // 5
        col = idx % 5
        cx0 = col_xs[col]
        cy0 = 480 + row * 129
        draw_grid_art(draw, num, cx0, cy0 + 2, cx0 + cell_w, cy0 + 52)
        draw_text_fit(draw, (cx0, cy0 + 57), f"{num} {place_topic}", f_gkick, kcol, max_w=cell_w)
        h_lines = wrap_lines(draw, head, f_ghead, cell_w)[:2]
        for li, line in enumerate(h_lines):
            draw.text((cx0, cy0 + 72 + li * 17), line, font=f_ghead, fill=INK)
        draw_text_fit(draw, (cx0, cy0 + 109), stand, f_gbody, MUTED, max_w=cell_w)
        if col < 4:
            gx = cx0 + cell_w + 6
            draw.line([gx, cy0 + 3, gx, cy0 + 123], fill=RULE, width=1)

    draw.line([x_left, 606, x_right, 606], fill=RULE, width=1)
    draw.line([x_left, 736, x_right, 736], fill=DARK_RULE, width=2)

    # 8. Foot (y 736-968): World Map left + ALSO ON FRIDAY right
    f_ftitle = font(F_SANS_B, 12)
    f_fcap = font(F_SANS, 10)
    map_x0, map_x1 = x_left, 280
    draw.text((map_x0, 742), "WHERE IT HAPPENED", font=f_ftitle, fill=INK)
    draw_world_map(draw, map_x0, 760, map_x1, 948)
    draw_text_fit(draw, ((map_x0 + map_x1) // 2, 952), "numbers match the stories", f_fcap, MUTED, max_w=262, anchor="mt")

    draw.line([290, 741, 290, 963], fill=RULE, width=1)

    also_x0 = 300
    col_w = 347
    also_cols = [also_x0, also_x0 + 359]
    draw.text((also_x0, 742), "ALSO ON FRIDAY 20 NOVEMBER 2026", font=f_ftitle, fill=RED)

    also_items = [
        "14 Washington — US sanctions 2 crime gangs. AppiSToS",
        "15 Washington — Trump pardons Pete Rose. AppiSToS",
        "16 Washington — White House fires cyber chief. Hindu",
        "17 Washington — 880k AI chips for China. SimpleLife",
        "18 Washington — $12bn Venezuela oil report. Paris Eye",
        "19 Paris — 4th weekend cost-of-living protest. Paris Eye",
        "20 Lilongwe — Malawi fuel crisis turns violent. NMH",
        "21 Warsaw — Poland $50bn US nuclear plan. NMH",
        "22 Menlo Park — Meta revises 2030 climate goals. NMH",
        "23 Brasília — Lula visits ailing Chief Raoni. NMH",
        "24 Prague — Czech leaders visit Israel. NMH",
        "25 New Delhi — Justice Varma resigns. NDTV",
        "26 Seoul — Choi to lead Samsung mobile. SimpleLife",
        "27 Mountain View — Gemini Mac control. SimpleLife",
        "28 Space — BepiColombo nears Mercury. Guardian",
        "29 Paris — IEA: datacentre CO2 +70% by '30. Guardian",
        "30 Worldwide — GTA VI out; 15.9m pre-orders.",
    ]
    f_also = font(F_SANS, 12)
    for i, item in enumerate(also_items):
        c = 0 if i < 9 else 1
        r = i if i < 9 else i - 9
        ax = also_cols[c]
        ay = 764 + r * 22
        draw_text_fit(draw, (ax, ay), item, f_also, INK, max_w=col_w)

    # 9. Bottom footer (y 968-1012)
    draw.line([x_left, 968, x_right, 968], fill=DARK_RULE, width=2)
    f_dc = font(F_SANS_B, 10)
    f_src = font(F_SANS, 10)
    dc_text = "DATE CHECK: every story on this page happened, or was first reported, on Friday 20 November 2026."
    src_text = "Sources: AnewZ, NPR, FXStreet, SimpleLife, AppiSToS, EIN Presswire, The Paris Eye, News Media House, Korea JoongAng Daily, stockbiz.vn, NDTV, The Hindu, Guardian, The Times of India."
    draw_text_fit(draw, (W // 2, 974), dc_text, f_dc, INK, max_w=usable_w, anchor="mt")
    draw_text_fit(draw, (W // 2, 991), src_text, f_src, MUTED, max_w=usable_w, anchor="mt")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
