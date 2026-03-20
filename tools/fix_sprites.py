"""
One-time script to remove black backgrounds from sprite PNGs.
Uses flood-fill from corners to replace background black with transparency,
preserving dark pixels that are part of the actual sprite.
"""
import os
from PIL import Image, ImageDraw

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
TOLERANCE = 40  # How close to black a pixel must be to count as background


def remove_background(image_path, tolerance=TOLERANCE):
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    # Mask of pixels to make transparent (flood-filled from corners)
    visited = set()
    queue = []

    # Seed from all four corners
    for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        queue.append((x, y))

    while queue:
        x, y = queue.pop()
        if (x, y) in visited:
            continue
        if x < 0 or x >= w or y < 0 or y >= h:
            continue

        r, g, b, a = pixels[x, y]
        # Check if pixel is "close to black" (background)
        if r <= tolerance and g <= tolerance and b <= tolerance:
            visited.add((x, y))
            pixels[x, y] = (0, 0, 0, 0)  # Make transparent
            # Expand to neighbors (4-connected)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited:
                    queue.append((nx, ny))
        else:
            visited.add((x, y))

    img.save(image_path)
    print(f"  Fixed: {os.path.basename(image_path)}")


def main():
    print("Removing black backgrounds from sprites...")
    for filename in os.listdir(ASSETS_DIR):
        if filename.endswith(".png"):
            remove_background(os.path.join(ASSETS_DIR, filename))
    print("Done!")


if __name__ == "__main__":
    main()
