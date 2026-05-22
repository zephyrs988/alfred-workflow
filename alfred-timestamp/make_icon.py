#!/usr/bin/env python3
"""Generate a crisp 256x256 clock icon for Alfred (no scaling distortion)."""

from math import cos, sin, pi
from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 256
CENTER = SIZE // 2
FACE_R = 98
BLUE = (51, 136, 255, 255)
BLUE_DARK = (32, 108, 220, 255)
WHITE = (255, 255, 255, 255)


def main():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # subtle round background
    draw.ellipse(
        (CENTER - FACE_R - 10, CENTER - FACE_R - 10, CENTER + FACE_R + 10, CENTER + FACE_R + 10),
        fill=(240, 247, 255, 255),
    )
    draw.ellipse(
        (CENTER - FACE_R, CENTER - FACE_R, CENTER + FACE_R, CENTER + FACE_R),
        fill=BLUE,
        outline=BLUE_DARK,
        width=4,
    )

    # hour ticks
    for i in range(12):
        angle = pi / 2 - i * (2 * pi / 12)
        x1 = CENTER + int((FACE_R - 18) * cos(angle))
        y1 = CENTER - int((FACE_R - 18) * sin(angle))
        x2 = CENTER + int((FACE_R - 6) * cos(angle))
        y2 = CENTER - int((FACE_R - 6) * sin(angle))
        draw.line((x1, y1, x2, y2), fill=WHITE, width=5)

    def hand(length, width, angle_deg, color=WHITE):
        angle = pi / 2 - angle_deg * pi / 180
        x = CENTER + int(length * cos(angle))
        y = CENTER - int(length * sin(angle))
        draw.line((CENTER, CENTER, x, y), fill=color, width=width)

    # 10:10 pose — classic icon look
    hand(52, 10, 50)
    hand(70, 7, 300)
    draw.ellipse((CENTER - 8, CENTER - 8, CENTER + 8, CENTER + 8), fill=WHITE)

    out = Path(__file__).resolve().parent / "icon.png"
    img.save(out, format="PNG", optimize=False)
    print(f"wrote {out} ({SIZE}x{SIZE})")


if __name__ == "__main__":
    main()
