# MIT License
#
# Copyright (c) 2026
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Create a video from a folder of numbered images."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

import cv2

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

NATURAL_KEY_RE = re.compile(r"(\d+|\D+)")


def natural_sort_key(name: str) -> tuple:
    parts = NATURAL_KEY_RE.findall(name)
    key = []
    for part in parts:
        if part.isdigit():
            key.append((0, int(part)))
        else:
            key.append((1, part.lower()))
    return tuple(key)


def gather_images(folder: Path) -> list[Path]:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")
    images = [path for path in folder.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS]
    images.sort(key=lambda p: natural_sort_key(p.name))
    return images


def write_video(images: list[Path], output_path: Path, fps: float, codec: str) -> None:
    first_image = cv2.imread(str(images[0]))
    if first_image is None:
        raise RuntimeError(f"Unable to read image: {images[0]}")

    height, width = first_image.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"Failed to open video writer for: {output_path}")

    for image_path in images:
        frame = cv2.imread(str(image_path))
        if frame is None:
            raise RuntimeError(f"Unable to read image: {image_path}")

        if frame.shape[:2] != (height, width):
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

        writer.write(frame)

    writer.release()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a video from a folder of numbered images.")
    parser.add_argument("folder", type=Path, help="Path to the folder with image frames.")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output video file path. If not specified, saves alongside the input folder using the folder name.")
    parser.add_argument(
        "-r", "--fps",
        type=float,
        default=30.0,
        help="Frames per second for the output video. Defaults to 30.")
    parser.add_argument(
        "-c", "--codec",
        default="mp4v",
        help="FourCC codec for the output video. Defaults to mp4v.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    images = gather_images(args.folder)
    if not images:
        print(f"No supported images found in {args.folder}.", file=sys.stderr)
        return 1

    if args.output is None:
        input_folder = args.folder
        parent = input_folder.parent
        base_name = input_folder.name
        output_path = parent / f"{base_name}.mp4"
        if output_path.exists():
            # Find the next available 4-digit number suffix
            pattern = re.compile(rf"{re.escape(base_name)}(\d{{4}})\.mp4$")
            existing = [p for p in parent.iterdir() if p.name.startswith(base_name) and p.suffix == '.mp4']
            numbers = []
            for p in existing:
                match = pattern.match(p.name)
                if match:
                    numbers.append(int(match.group(1)))
            if numbers:
                next_num = max(numbers) + 1
            else:
                next_num = 1
            output_path = parent / f"{base_name}{next_num:04d}.mp4"
    else:
        output_path = args.output

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Building video from {len(images)} frames...")
    print(f"Input folder: {args.folder}")
    print(f"Output file: {output_path}")
    print(f"FPS: {args.fps}")
    print(f"Codec: {args.codec}")

    write_video(images, output_path, args.fps, args.codec)
    print("Video created successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
