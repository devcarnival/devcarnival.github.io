#!/usr/bin/env python3
"""
Offline asset step for the Dev Carnival hero scrub. NOT part of the Hugo build.

Reads the raw 1280x720 JPEG frame sequence, prepends a synthetic "empty asphalt
grid" lead-in that dissolves into frame 1, and writes two WebP sets:

    static/frames/dc-0001.webp ... 1280x720  (desktop)
    static/frames-sm/dc-0001.webp ...  768x432  (mobile / narrow viewports)

Also writes the reduced-motion poster and the 1200x630 social card.

Run once, commit the output, never again:

    python3 tools/build-frames.py /path/to/raw-frames

Requires Pillow. Nothing in `hugo` or the page runtime depends on this file.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

from make_brand_mark import render_tile

# --- tunables ---------------------------------------------------------------

LEAD_IN = 20  # synthetic frames: bare asphalt -> frame 1
ASPHALT = (18, 18, 20)  # #121214 — must match --dc-asphalt in style.css

# The HD render (2026-08-22 drone pass) carries far more high-frequency detail
# than the first set — bokeh, string lights, signage text — so the old 72/62
# quality banded visibly on those; bumped until a spot-check crop of the
# ferris wheel neon stopped showing blocking.
FULL_W, FULL_Q = 1280, 80
SMALL_W, SMALL_Q = 768, 68

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FULL = os.path.join(REPO, "static", "frames")
OUT_SMALL = os.path.join(REPO, "static", "frames-sm")
OUT_IMG = os.path.join(REPO, "static", "img")

# The renderer stamped a badge into the lower right of every footage frame. On
# the page a brand tile covers it, positioned and slid in by carnival-hero.js
# (see BUG_BOX there — keep these two in step). The poster and the social card
# are shown with no JS in play, so the tile is baked into them here instead.
BUG_BOX = (0.8875, 0.8000, 0.9250, 0.8667)  # u0, v0, u1, v1 of the raw frame
BUG_PAD = 0.010  # extra cover each side, as a fraction of image width
MARK_PNG = os.path.join(OUT_IMG, "dc-mark.png")


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def asphalt_grid(w, h):
    """Bare isometric ground plane: deep asphalt, faint diamond grid, vignette."""
    base = Image.new("RGB", (w, h), ASPHALT)
    grid = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(grid)

    step = w // 20
    slope = 0.5  # ~26.6deg — reads as a 2:1 isometric floor
    span = int(w + h / slope) + step

    # two line families crossing at +/- the iso angle
    for sign in (1, -1):
        for i in range(-span, span, step):
            # cyan tint every 4th line, otherwise a cool structural line
            accent = (i // step) % 4 == 0
            colour = (34, 224, 255, 62) if accent else (78, 80, 100, 78)
            d.line(
                [(i, h), (i + int(h / slope) * sign, 0)],
                fill=colour,
                width=2 if accent else 1,
            )

    # fade the grid out toward the horizon so it sits like a ground plane,
    # and out at the left/right edges so it doesn't read as a flat rectangle
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for y in range(h):
        t = y / (h - 1)
        md.line([(0, y), (w, y)], fill=int(255 * smoothstep((t - 0.30) / 0.55)))
    edge = Image.new("L", (w, h), 0)
    ed = ImageDraw.Draw(edge)
    for x in range(w):
        t = abs(x / (w - 1) - 0.5) * 2
        ed.line([(x, 0), (x, h)], fill=int(255 * (1 - smoothstep((t - 0.55) / 0.45))))
    from PIL import ImageChops
    combined = ImageChops.multiply(mask, edge)
    grid.putalpha(ImageChops.multiply(grid.getchannel("A"), combined))

    out = Image.alpha_composite(base.convert("RGBA"), grid).convert("RGB")

    # faint magenta/cyan horizon glow — the carnival about to switch on
    glow = Image.new("RGB", (w, h), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([w * 0.12, h * 0.10, w * 0.88, h * 0.62], fill=(26, 10, 34))
    gd.ellipse([w * 0.30, h * 0.18, w * 0.70, h * 0.50], fill=(10, 26, 34))
    glow = glow.filter(ImageFilter.GaussianBlur(w / 12))
    return ImageChops.add(out, glow)


def zoomed(im, factor):
    """Centre zoom without changing dimensions."""
    if factor <= 1.0:
        return im
    w, h = im.size
    cw, ch = int(w / factor), int(h / factor)
    box = ((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2)
    return im.crop(box).resize((w, h), Image.LANCZOS)


def save_pair(im, index):
    full = im if im.width == FULL_W else im.resize(
        (FULL_W, round(im.height * FULL_W / im.width)), Image.LANCZOS
    )
    full.save(
        os.path.join(OUT_FULL, f"dc-{index:04d}.webp"),
        "WEBP", quality=FULL_Q, method=6,
    )
    small = im.resize((SMALL_W, round(im.height * SMALL_W / im.width)), Image.LANCZOS)
    small.save(
        os.path.join(OUT_SMALL, f"dc-{index:04d}.webp"),
        "WEBP", quality=SMALL_Q, method=6,
    )


def stamp_bug(im, box):
    """Composite the brand tile over the badge, given its pixel box in `im`.

    The tile is rendered at the size it is pasted at rather than scaled down
    afterwards: its border is a literal 1px and resampling smears it into grey.
    """
    x0, y0, x1, y1 = box
    pad = BUG_PAD * im.width
    side = round(max(x1 - x0, y1 - y0) + pad * 2)
    left = round(min(max((x0 + x1 - side) / 2, 0), im.width - side))
    top = round(min(max((y0 + y1 - side) / 2, 0), im.height - side))

    mark = Image.open(MARK_PNG).convert("RGBA")
    im.paste(render_tile(mark, side).convert("RGB"), (left, top))
    return im


def write_stills(last):
    """Reduced-motion poster + 1200x630 social card, both with the tile baked in."""
    u0, v0, u1, v1 = BUG_BOX

    # poster: a plain resize, so the normalised box carries straight over
    poster = last.resize((1600, round(last.height * 1600 / last.width)), Image.LANCZOS)
    stamp_bug(poster, (u0 * poster.width, v0 * poster.height,
                       u1 * poster.width, v1 * poster.height))
    poster.save(os.path.join(OUT_IMG, "hero-static.webp"), "WEBP",
                quality=82, method=6)

    full = stamp_bug(last.copy(), (u0 * last.width, v0 * last.height,
                                   u1 * last.width, v1 * last.height))
    full.save(os.path.join(OUT_IMG, "hero-static.jpg"), "JPEG", quality=82,
              optimize=True, progressive=True)

    # social card: cover-crop, so the box shifts by the crop offset
    card_w, card_h = 1200, 630
    scale = max(card_w / last.width, card_h / last.height)
    tmp = last.resize((round(last.width * scale), round(last.height * scale)),
                      Image.LANCZOS)
    left = (tmp.width - card_w) // 2
    top = (tmp.height - card_h) // 2
    card = tmp.crop((left, top, left + card_w, top + card_h))
    stamp_bug(card, (u0 * tmp.width - left, v0 * tmp.height - top,
                     u1 * tmp.width - left, v1 * tmp.height - top))
    # baseof.html reads img/social-card.jpg for og:image + twitter:image
    card.save(os.path.join(OUT_IMG, "social-card.jpg"), "JPEG", quality=86,
              optimize=True, progressive=True)


def main():
    if len(sys.argv) < 2:
        sys.exit(f"usage: {sys.argv[0]} <raw-frames-dir>")
    raw_dir = sys.argv[1]
    raw = sorted(
        os.path.join(raw_dir, f)
        for f in os.listdir(raw_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    if not raw:
        sys.exit(f"no frames found in {raw_dir}")

    for d in (OUT_FULL, OUT_SMALL, OUT_IMG):
        os.makedirs(d, exist_ok=True)

    first = Image.open(raw[0]).convert("RGB")
    w, h = first.size
    plate = asphalt_grid(w, h)

    # 1..LEAD_IN — the grounds materialising out of the dark
    for i in range(LEAD_IN):
        t = smoothstep(i / LEAD_IN)
        blend = Image.blend(plate, zoomed(first, 1.0 + 0.07 * (1 - t)), t ** 1.35)
        save_pair(blend, i + 1)
        print(f"lead-in {i + 1}/{LEAD_IN}", flush=True)

    # LEAD_IN+1.. — the flythrough itself
    for i, path in enumerate(raw):
        save_pair(Image.open(path).convert("RGB"), LEAD_IN + i + 1)
        if (i + 1) % 20 == 0 or i == len(raw) - 1:
            print(f"flythrough {i + 1}/{len(raw)}", flush=True)

    total = LEAD_IN + len(raw)

    # derived stills: the final wide shot with the arched sign
    write_stills(Image.open(raw[-1]).convert("RGB"))

    print(f"\ndone: {total} frames -> static/frames + static/frames-sm")
    print(f"set DC_FRAME_COUNT = {total} in static/js/carnival-hero.js")


if __name__ == "__main__":
    main()
