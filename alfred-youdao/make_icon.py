#!/usr/bin/env python3
"""Generate 256x256 translate icon for Alfred workflow."""

from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 256
CENTER = SIZE // 2


def main():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # background
    draw.ellipse((28, 28, 228, 228), fill=(232, 248, 240, 255))
    draw.ellipse((40, 40, 216, 216), fill=(46, 168, 98, 255), outline=(30, 130, 76, 255), width=4)

    # stylized 译
    draw.rectangle((88, 78, 168, 98), fill=(255, 255, 255, 255))
    draw.rectangle((118, 98, 138, 178), fill=(255, 255, 255, 255))
    draw.polygon([(88, 118), (168, 118), (128, 168)], fill=(255, 255, 255, 255))

    out = Path(__file__).resolve().parent / "icon.png"
    img.save(out, format="PNG", optimize=False)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
