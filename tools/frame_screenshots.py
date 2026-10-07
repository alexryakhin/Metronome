#!/usr/bin/env python3
"""Puts simulator screenshots into tools/iphone-frame.webp.

The frame's screen is transparent; it's found by flood-filling from the centre, and that exact
shape (rounded corners, Dynamic Island cut-out) becomes the mask. Screenshots are scaled to cover
the screen without distortion (aspect is preserved, any overflow is cropped evenly).

Usage: python3 tools/frame_screenshots.py raw/today.png raw/calendar.png ...
Writes assets/img/<name>.webp next to the site.
"""
import collections
import pathlib
import sys

from PIL import Image, ImageChops

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAME = Image.open(ROOT / "tools/iphone-frame.webp").convert("RGBA")
W, H = FRAME.size


def screen_mask():
    alpha = FRAME.getchannel("A").load()
    mask = Image.new("L", FRAME.size, 0)
    m = mask.load()
    queue = collections.deque([(W // 2, H // 2)])
    while queue:
        x, y = queue.popleft()
        if not (0 <= x < W and 0 <= y < H) or m[x, y] or alpha[x, y] > 128:
            continue
        m[x, y] = 255
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return mask


MASK = screen_mask()
BOX = MASK.getbbox()  # (left, top, right, bottom)


def frame(src: pathlib.Path) -> Image.Image:
    shot = Image.open(src).convert("RGB")
    bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
    scale = max(bw / shot.width, bh / shot.height)
    resized = shot.resize((round(shot.width * scale), round(shot.height * scale)), Image.LANCZOS)
    left = (resized.width - bw) // 2
    top = (resized.height - bh) // 2
    resized = resized.crop((left, top, left + bw, top + bh))

    canvas = Image.new("RGBA", FRAME.size, (0, 0, 0, 0))
    canvas.paste(resized, BOX[:2])
    # Keep only the screen shape, then lay the bezel (and island) on top.
    canvas.putalpha(ImageChops.multiply(canvas.getchannel("A"), MASK))
    return Image.alpha_composite(canvas, FRAME)


if __name__ == "__main__":
    bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
    print(f"frame {W}x{H}, screen {bw}x{bh} at {BOX[:2]}, aspect {bw / bh:.4f}")
    for arg in sys.argv[1:]:
        src = pathlib.Path(arg)
        out = ROOT / "assets/img" / f"{src.stem}.webp"
        frame(src).save(out, "WEBP", quality=88, method=6)
        print("wrote", out.relative_to(ROOT), f"(source {Image.open(src).size}, aspect {Image.open(src).width / Image.open(src).height:.4f})")
