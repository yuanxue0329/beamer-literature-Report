"""Read image geometry and estimate outer whitespace without changing image files.

Requires Pillow. Output is JSON, with pixel coordinates explicitly separate from
physical TeX crop units. A reported crop is a candidate for visual inspection.
"""

import argparse
import json
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageOps
except ImportError:
    raise SystemExit("Pillow is required to inspect images; no files were changed.")


RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def declared_dpi(value, orientation):
    if not isinstance(value, (tuple, list)) or len(value) < 2:
        return None
    try:
        x, y = float(value[0]), float(value[1])
    except (TypeError, ValueError, OverflowError):
        return None
    if not (math.isfinite(x) and math.isfinite(y) and x > 0 and y > 0):
        return None
    return [y, x] if orientation in (5, 6, 7, 8) else [x, y]


def inspect_image(path, threshold):
    with Image.open(path) as source:
        raw_size = list(source.size)
        orientation = source.getexif().get(274, 1)
        dpi = declared_dpi(source.info.get("dpi"), orientation)
        frame_count = getattr(source, "n_frames", 1)
        normalized = ImageOps.exif_transpose(source)
        rgba = normalized.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        rgb = Image.alpha_composite(background, rgba).convert("RGB")
        width, height = rgb.size
        red, green, blue = rgb.split()
        minimum_channel = ImageChops.darker(ImageChops.darker(red, green), blue)
        ink = minimum_channel.point(lambda value: 255 if value < threshold else 0)
        bbox = ink.getbbox()

        result = {
            "path": str(path.resolve()),
            "format": source.format,
            "raw_pixel_size": raw_size,
            "exif_orientation": orientation,
            "pixel_size": [width, height],
            "aspect_ratio": round(width / height, 6),
            "coordinate_space": "EXIF-normalized display pixels; bbox right/bottom exclusive",
            "frames": frame_count,
            "inspected_frame": 0,
            "declared_dpi": dpi,
            "white_threshold": threshold,
            "content_bbox_px": list(bbox) if bbox else None,
            "suggested_outer_trim_px_lbrt": None,
            "outer_margin_area_fraction": None,
            "trim_bp_from_declared_dpi_lbrt": None,
            "candidate_only": True,
        }
        if bbox:
            left, top, right_edge, bottom_edge = bbox
            right, bottom = width - right_edge, height - bottom_edge
            result["suggested_outer_trim_px_lbrt"] = [left, bottom, right, top]
            content_width, content_height = right_edge - left, bottom_edge - top
            result["content_aspect_ratio"] = round(content_width / content_height, 6)
            result["outer_margin_area_fraction"] = round(
                1 - (content_width * content_height) / (width * height), 6
            )
            if dpi:
                xdpi, ydpi = dpi
                result["trim_bp_from_declared_dpi_lbrt"] = [
                    round(left * 72 / xdpi, 4),
                    round(bottom * 72 / ydpi, 4),
                    round(right * 72 / xdpi, 4),
                    round(top * 72 / ydpi, 4),
                ]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Raster images or image directories")
    parser.add_argument("--white-threshold", type=int, default=245)
    parser.add_argument("--recursive", action="store_true", help="Scan directory descendants")
    args = parser.parse_args()
    if not 1 <= args.white_threshold <= 255:
        parser.error("--white-threshold must be between 1 and 255")

    files = []
    for raw_path in args.paths:
        path = Path(raw_path).expanduser()
        if path.is_dir():
            candidates = path.rglob("*") if args.recursive else path.iterdir()
            files.extend(sorted(
                (p for p in candidates if p.is_file() and p.suffix.lower() in RASTER_SUFFIXES),
                key=lambda p: str(p).casefold(),
            ))
        else:
            files.append(path)

    results, seen = [], set()
    for path in files:
        identity = path.resolve()
        if identity in seen:
            continue
        seen.add(identity)
        try:
            if path.suffix.lower() not in RASTER_SUFFIXES:
                raise ValueError("Expected a supported raster image")
            results.append(inspect_image(path, args.white_threshold))
        except (OSError, ValueError, SyntaxError, Image.DecompressionBombError) as error:
            results.append({"path": str(identity), "error": str(error)})

    print(json.dumps({"images": results, "source_images_modified": False}, indent=2, ensure_ascii=True))
    return 1 if any("error" in result for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
