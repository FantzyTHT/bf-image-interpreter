import sys
from pathlib import Path
from PIL import Image

TARGET_HEIGHT = 64

def image_to_brainfuck(image_path):
    img = Image.open(image_path).convert("L")

    # Keep aspect ratio, fixed height
    scale = TARGET_HEIGHT / img.height
    new_width = max(1, int(img.width * scale))

    img = img.resize(
        (new_width, TARGET_HEIGHT),
        Image.Resampling.LANCZOS
    )

    pixels = list(img.getdata())

    bf = []
    current = 0

    for pixel in pixels:
        diff = pixel - current

        if diff > 0:
            bf.append("+" * diff)
        elif diff < 0:
            bf.append("-" * (-diff))

        bf.append(".")
        current = pixel

    return "".join(bf), new_width


def main():
    if len(sys.argv) < 2:
        return

    image_file = Path(sys.argv[1])

    if not image_file.exists():
        return

    code, width = image_to_brainfuck(image_file)

    # =========================
    # OUTPUT ALWAYS NEXT TO SCRIPT
    # =========================
    script_dir = Path(__file__).resolve().parent

    base_name = image_file.stem

    # =========================
    # NAMING RULES
    # =========================
    if width == 64:
        output_name = f"{base_name}.bf"
    else:
        output_name = f"{base_name}({width}).bf"

    output_file = script_dir / output_name

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(code)


if __name__ == "__main__":
    main()