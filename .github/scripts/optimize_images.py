# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow", "pyyaml"]
# ///
import pathlib

import yaml
from PIL import Image, ImageOps

CONTENT_DIR = pathlib.Path("content")
IMG_DIR = CONTENT_DIR / "img"
HERO_MAX = 2560
DEFAULT_MAX = 1400
EXTENSIONS = {".jpg", ".jpeg", ".png"}


def hero_path():
    metadata = yaml.safe_load((CONTENT_DIR / "_metadata.yml").read_text())
    return CONTENT_DIR / metadata["hero_image"].lstrip("/")


def optimize(path, max_side):
    with Image.open(path) as src:
        if max(src.size) <= max_side and not src.getexif():
            return False
        img = ImageOps.exif_transpose(src)
        img.thumbnail((max_side, max_side), Image.LANCZOS)

    if path.suffix.lower() == ".png":
        if img.mode == "RGBA" and img.getchannel("A").getextrema() == (255, 255):
            img = img.convert("RGB")
        img.save(path, optimize=True)
    else:
        img.convert("RGB").save(path, quality=82, optimize=True, progressive=True)
    return True


def main():
    hero = hero_path()
    for path in sorted(IMG_DIR.iterdir()):
        if path.suffix.lower() not in EXTENSIONS:
            continue
        before = path.stat().st_size
        max_side = HERO_MAX if path == hero else DEFAULT_MAX
        if optimize(path, max_side):
            after = path.stat().st_size
            print(f"{path.name}: {before / 1e6:.2f} MB -> {after / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
