#!/usr/bin/env python3
"""Generate 256x256 UUID icon for Alfred workflow."""

from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 256
CENTER = SIZE // 2


def main():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.ellipse((28, 28, 228, 228), fill=(245, 240, 255, 255))
    draw.ellipse((40, 40, 216, 216), fill=(120, 86, 220, 255), outline=(90, 60, 180, 255), width=4)

    # stylized hex blocks
    blocks = [
        (78, 88, 118, 108),
        (138, 88, 178, 108),
        (78, 128, 118, 148),
        (138, 128, 178, 148),
        (98, 168, 158, 188),
    ]
    for box in blocks:
        draw.rounded_rectangle(box, radius=6, fill=(255, 255, 255, 255))

    out = Path(__file__).resolve().parent / "icon.png"
    img.save(out, format="PNG", optimize=False)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
