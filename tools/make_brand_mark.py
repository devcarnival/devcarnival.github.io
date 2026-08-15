#!/usr/bin/env python3
"""
Derive every Dev Carnival brand asset from the one logo lockup.

Offline, one-time. NOT part of the Hugo build.

  static/img/dc-mark.png   transparent monogram — the hero brand tile draws it
  static/img/dc-logo.png   transparent full lockup (monogram + wordmark + line)
  static/favicon*, apple-icon*, android-icon*, ms-icon*, apple-touch-icon
                           the app icon set, as dark tiles

The source lockup is three stacked bands — monogram, "DEV CARNIVAL" wordmark,
tagline. dc-mark.png is band 0 alone; the wordmark is illegible at tile size.

Icons are dark tiles rather than a transparent mark: the mark is white-on-black,
so on a light browser tab strip a transparent version would vanish. They also
use a tighter crop than dc-mark.png (see core_crop) because the full monogram's
outer arms turn to mush at 16px.

The hero tile is built two ways that must agree: .dc-hero__bug in style.css
draws it live, and build-frames.py bakes it into the poster and social card for
the no-JS path. render_tile() here is the one definition of it, imported there —
hence the importable underscored filename.

Usage:  python3 tools/make_brand_mark.py [path/to/logo.png]
"""

import os
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(REPO, "static")
OUT = os.path.join(STATIC, "img")
OUT_TMP = tempfile.gettempdir()

DEFAULT_SRC = os.path.expanduser(
    "~/Downloads/ChatGPT Image Aug 15, 2026, 05_38_15 PM.png"
)

MARK_PX = 256           # monogram export width
LOGO_PX = 768           # full lockup export width
TILE_PX = 192           # hero tile size
INK = 40                # luminance above which a pixel counts as ink
BLACK_FLOOR = 10 / 255  # the lockup's backdrop is (3,3,7), not pure black

# Must match style.css exactly or the baked tile will not match the CSS one.
ASPHALT = (18, 18, 20)       # --dc-asphalt
HAIRLINE = (58, 58, 70)      # --dc-line-bright, same as .dc-panel
TILE_PAD = 0.18              # mark inset, fraction of tile size

ICON_PAD = 0.08              # icons crop tighter than the hero tile
ICON_CORE = 1.72             # core crop width, as a multiple of the star's

# Every icon the site references: baseof.html links favicon.ico/-16/-32 and
# apple-touch-icon, manifest.json lists the android set, browserconfig.xml the
# ms set, and iOS/Android probe the rest by convention.
ICONS = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "favicon-96x96.png": 96,
    "apple-icon-57x57.png": 57,
    "apple-icon-60x60.png": 60,
    "apple-icon-72x72.png": 72,
    "apple-icon-76x76.png": 76,
    "apple-icon-114x114.png": 114,
    "apple-icon-120x120.png": 120,
    "apple-icon-144x144.png": 144,
    "apple-icon-152x152.png": 152,
    "apple-icon-180x180.png": 180,
    "apple-icon.png": 180,
    "apple-icon-precomposed.png": 180,
    "apple-touch-icon.png": 180,
    "android-icon-36x36.png": 36,
    "android-icon-48x48.png": 48,
    "android-icon-72x72.png": 72,
    "android-icon-96x96.png": 96,
    "android-icon-144x144.png": 144,
    "android-icon-192x192.png": 192,
    "ms-icon-70x70.png": 70,
    "ms-icon-144x144.png": 144,   # not in browserconfig.xml, but shipped
    "ms-icon-150x150.png": 150,
    "ms-icon-310x310.png": 310,
}
ICO_SIZES = (16, 32, 48)


def ink_bands(gray):
    """Vertical runs of rows containing ink, top to bottom."""
    rows = (gray > INK).any(axis=1)
    bands, start = [], None
    for y, v in enumerate(rows):
        if v and start is None:
            start = y
        elif not v and start is not None:
            bands.append((start, y))
            start = None
    if start is not None:
        bands.append((start, len(rows)))
    return bands


def key_alpha(im):
    """Key the lockup's near-black backdrop out to alpha.

    The lockup is a bright mark on near-black, i.e. already premultiplied
    against black. alpha = max(r,g,b) recovers coverage; dividing it back out
    recovers the colour, so the gradient star keeps its saturation instead of
    going translucent. The backdrop is (3,3,7) rather than pure black, so lift
    that floor off first or every background pixel keeps ~3% alpha and the crop
    box shows as a faint rectangle wherever the mark is composited.
    """
    a = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    alpha = np.clip((a.max(axis=2) - BLACK_FLOOR) / (1.0 - BLACK_FLOOR), 0.0, 1.0)
    rgb = np.clip(a / np.maximum(alpha, 1e-4)[..., None], 0.0, 1.0)
    out = np.dstack([rgb, alpha[..., None]])
    return Image.fromarray((out * 255).round().astype("uint8"), "RGBA")


def _bands(src):
    im = Image.open(src).convert("RGB")
    gray = np.asarray(im.convert("L"), dtype=np.float32)
    bands = ink_bands(gray)
    if not bands:
        sys.exit(f"no ink found in {src}")
    return im, gray, bands


def _crop(im, gray, top, bottom, width):
    cols = np.nonzero((gray[top:bottom, :] > INK).any(axis=0))[0]
    box = (int(cols.min()), top, int(cols.max()) + 1, bottom)
    keyed = key_alpha(im.crop(box))
    h = round(keyed.height * width / keyed.width)
    return keyed.resize((width, h), Image.LANCZOS), box


def extract_mark(src):
    """The monogram alone — band 0 of the lockup."""
    im, gray, bands = _bands(src)
    return _crop(im, gray, bands[0][0], bands[0][1], MARK_PX)


def extract_logo(src):
    """The whole lockup: monogram, wordmark and tagline, trimmed to its ink."""
    im, gray, bands = _bands(src)
    return _crop(im, gray, bands[0][0], bands[-1][1], LOGO_PX)


def core_crop(mark):
    """A squarer, bolder window on the monogram, for small icons.

    Anchored on the gradient star — the one saturated element — rather than on
    hardcoded pixels, so re-exporting the lockup at another size still lands.
    """
    a = np.asarray(mark, dtype=np.float32)
    rgb, alpha = a[..., :3], a[..., 3]
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    ys, xs = np.nonzero((sat > 0.25) & (alpha > INK))
    if not len(xs):
        return mark

    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    half = (xs.max() - xs.min() + 1) * ICON_CORE / 2
    return mark.crop((round(cx - half), round(cy - half),
                      round(cx + half), round(cy + half)))


def _compose(src, size, pad, fill=ASPHALT):
    """`src` centred on a `size` square of `fill`, inset by `pad` of the side."""
    out = Image.new("RGBA", (size, size), fill + (255,))
    inner = max(1, round(size * (1 - 2 * pad)))
    w, h = inner, max(1, round(src.height * inner / src.width))
    if h > inner:
        h, w = inner, max(1, round(src.width * inner / src.height))
    out.alpha_composite(src.resize((w, h), Image.LANCZOS),
                        ((size - w) // 2, (size - h) // 2))
    return out


def render_tile(mark, size=TILE_PX):
    """The hero tile as CSS draws it: asphalt fill, 1px hairline, mark centred.

    Render at the size you will paste at — the hairline is a literal 1px, so
    scaling a tile afterwards softens the border into a grey smear.
    """
    tile = _compose(mark, size, TILE_PAD)
    ImageDraw.Draw(tile).rectangle(
        [0, 0, size - 1, size - 1], outline=HAIRLINE + (255,), width=1
    )
    return tile


def render_icon(core, size):
    """An app icon: the core crop on asphalt, no hairline.

    The hero tile's hairline exists to separate it from the frame behind it; an
    icon has no backdrop to separate from, and at 16px a 1px border is 12% of
    the glyph's room.
    """
    return _compose(core, size, ICON_PAD)


def write_icons(mark):
    core = core_crop(mark)
    for name, size in ICONS.items():
        # RGB, not RGBA: these are opaque tiles, and an alpha channel on an
        # apple-touch-icon makes iOS composite it onto black anyway.
        render_icon(core, size).convert("RGB").save(
            os.path.join(STATIC, name), "PNG", optimize=True
        )

    # Each .ico frame is rendered from the mark rather than downscaled from one
    # bitmap — Pillow uses an exact-size append_images match verbatim. The base
    # image has to be the largest: Pillow drops any requested size bigger than
    # it, so leading with the 16px frame silently yields a one-frame icon.
    frames = sorted((render_icon(core, s).convert("RGBA") for s in ICO_SIZES),
                    key=lambda f: -f.width)
    frames[0].save(os.path.join(STATIC, "favicon.ico"), "ICO",
                   sizes=[(s, s) for s in ICO_SIZES], append_images=frames[1:])
    return len(ICONS) + 1


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    if not os.path.exists(src):
        sys.exit(f"logo not found: {src}\nusage: {sys.argv[0]} [logo.png]")

    os.makedirs(OUT, exist_ok=True)
    mark, box = extract_mark(src)
    mark.save(os.path.join(OUT, "dc-mark.png"), "PNG", optimize=True)

    logo, logo_box = extract_logo(src)
    logo.save(os.path.join(OUT, "dc-logo.png"), "PNG", optimize=True)

    written = write_icons(mark)

    # previews of the composed tile and the smallest icon, so a bad key or a
    # smeared hairline is visible without rebuilding the frames; not shipped
    render_tile(mark).save(os.path.join(OUT_TMP, "dc-tile-preview.png"), "PNG")
    render_icon(core_crop(mark), 32).resize((256, 256), Image.NEAREST).save(
        os.path.join(OUT_TMP, "dc-icon-preview.png"), "PNG"
    )

    print(f"source     {src}")
    print(f"monogram   cropped {box} -> {mark.size}")
    print(f"lockup     cropped {logo_box} -> {logo.size}")
    print(f"wrote      static/img/dc-mark.png  static/img/dc-logo.png")
    print(f"           {written} icons in static/")
    print(f"preview    {OUT_TMP}/dc-tile-preview.png  {OUT_TMP}/dc-icon-preview.png")


if __name__ == "__main__":
    main()
