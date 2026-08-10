#!/usr/bin/env python3
"""Turns the app's capture frames into web assets.

    ./tools/process-shots.py [source-directory]

Source defaults to `../aura-ios/build/screenshots`, which is what `Tools/screenshots.sh` writes.
Nothing here retouches the app's pixels: frames are resized and re-encoded, and that is all. If a
number in one of these looks wrong, it is wrong in the app — fix it there and recapture.

The site draws its own iPhone around each of these in CSS, so what goes out is the screen and
nothing else: no bezel, no rounded corners, no shadow. Baking any of that in would fight the
frame the page draws and would double up on the corner radius.

Two widths per shot, because a 1320px-wide PNG is between one and three megabytes and this is a
page someone opens on a phone, quite possibly to read the privacy policy before installing
anything. WebP at quality 80 lands the whole set in the low hundreds of kilobytes with no visible
loss on flat UI.

Only the light frames are used. Aura is a light product and the screenshots sit comfortably on
either page ground; carrying a dark set as well would double the assets to serve a case nobody
has asked for.
"""

import pathlib
import shutil
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT.parent / "aura-ios" / "build" / "screenshots"
OUT = ROOT / "shots"

# The frames the site actually shows, with the name each gets on the web.
WANTED = {
    "01-today.png": "today",
    "05-medications.png": "medications",
    "07-insights-weather.png": "weather",
    "04-insights-patterns.png": "patterns",
    "08-doctor-mode.png": "doctor",
}

# 1x and 2x for a phone whose screen renders at up to about 350 CSS pixels wide.
WIDTHS = (360, 720)


def main() -> int:
    source = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    if not source.is_dir():
        print(f"No capture directory at {source}", file=sys.stderr)
        return 1

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    total = 0
    for filename, stem in WANTED.items():
        frame = source / filename
        if not frame.is_file():
            print(f"  missing: {filename}", file=sys.stderr)
            continue

        image = Image.open(frame).convert("RGB")
        for width in WIDTHS:
            height = round(image.height * width / image.width)
            suffix = "" if width == WIDTHS[0] else f"@{width // WIDTHS[0]}x"
            target = OUT / f"{stem}{suffix}.webp"
            image.resize((width, height), Image.LANCZOS).save(
                target, "WEBP", quality=80, method=6
            )
            total += target.stat().st_size
            print(f"  {target.name:24s} {width:4d}px  {target.stat().st_size / 1024:6.0f} KB")

    print(f"\n{total / 1024:.0f} KB total in {OUT}")
    print(f"aspect ratio {image.width}:{image.height} -> use in .phone-screen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
