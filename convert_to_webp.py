import os
import argparse
from pathlib import Path
from PIL import Image
from tqdm import tqdm

def get_image_files(input_dir):
    """
    Returns a list of all image files in the directory and its subdirectories.
    """
    extensions = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.gif')
    image_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(extensions):
                image_files.append(Path(root) / file)
    return image_files

FORMATS = {
    "webp": ("WEBP", ".webp"),
    "jpg": ("JPEG", ".jpg"),
    "jpeg": ("JPEG", ".jpeg"),
    "png": ("PNG", ".png"),
    "bmp": ("BMP", ".bmp"),
    "tiff": ("TIFF", ".tiff"),
    "gif": ("GIF", ".gif"),
}

def process_image(img_path, output_path, max_landscape_width, max_portrait_height, quality, overwrite, pil_format):
    """
    Processes a single image: resizes if needed and converts to the target format.
    """
    if output_path.exists() and not overwrite:
        return "skipped"

    try:
        with Image.open(img_path) as img:
            # Handle orientation from EXIF
            try:
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass

            width, height = img.size
            
            # Determine if image is landscape or portrait
            is_landscape = width >= height
            
            needs_resize = False
            new_width, new_height = width, height

            if is_landscape:
                if width > max_landscape_width:
                    ratio = max_landscape_width / float(width)
                    new_width = max_landscape_width
                    new_height = int(float(height) * ratio)
                    needs_resize = True
            else:
                if height > max_portrait_height:
                    ratio = max_portrait_height / float(height)
                    new_height = max_portrait_height
                    new_width = int(float(width) * ratio)
                    needs_resize = True

            if needs_resize:
                # Use Resampling.LANCZOS for high-quality downsampling
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # JPEG doesn't support an alpha channel
            if pil_format == "JPEG" and img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")

            save_kwargs = {}
            if pil_format in ("WEBP", "JPEG"):
                save_kwargs["quality"] = quality

            img.save(output_path, pil_format, **save_kwargs)
            return "converted"
    except Exception as e:
        return f"error: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Convert images to WebP (or another format) with optional resizing.")
    parser.add_argument("input", nargs='+', help="Input directory path(s) - one or more directories")
    parser.add_argument("--output", "-o", help="Output directory path (default: input_<format>)")
    parser.add_argument("--format", "-f", choices=sorted(FORMATS.keys()), default="webp", help="Output format/extension (default: webp)")
    parser.add_argument("--max-landscape-width", type=int, default=1920, help="Max width for landscape images (default: 1920)")
    parser.add_argument("--max-portrait-height", type=int, default=1080, help="Max height for portrait images (default: 1080)")
    parser.add_argument("--quality", "-q", type=int, default=80, help="Output quality 0-100, used for webp/jpg (default: 80)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()

    pil_format, out_extension = FORMATS[args.format]

    input_paths = [Path(p).resolve() for p in args.input]
    
    # Validate all input directories
    for p in input_paths:
        if not p.is_dir():
            print(f"Error: {p} is not a valid directory.")
            return

    # Determine output base directory
    if args.output:
        output_base = Path(args.output).resolve()
    else:
        if len(input_paths) == 1:
            output_base = input_paths[0].with_name(f"{input_paths[0].name}_{args.format}")
        else:
            output_base = Path("output")
    
    print(f"Scanning {len(input_paths)} director{'y' if len(input_paths) == 1 else 'ies'}...")
    
    all_image_files = []
    for input_path in input_paths:
        files = get_image_files(input_path)
        all_image_files.extend([(f, input_path) for f in files])
        print(f"  {input_path}: {len(files)} images")
    
    if not all_image_files:
        print("No image files found.")
        return

    print(f"Found {len(all_image_files)} images total. Starting conversion...")
    
    stats = {"converted": 0, "skipped": 0, "error": 0}
    errors = []

    for img_file, input_dir in tqdm(all_image_files, desc="Converting", unit="file"):
        # Calculate relative path to maintain structure
        rel_path = img_file.relative_to(input_dir)
        # Output structure: output_base / input_dir_name / relative_path
        out_file = output_base / input_dir.name / rel_path.with_suffix(out_extension)

        result = process_image(
            img_file,
            out_file,
            args.max_landscape_width,
            args.max_portrait_height,
            args.quality,
            args.overwrite,
            pil_format
        )
        
        if result == "converted":
            stats["converted"] += 1
        elif result == "skipped":
            stats["skipped"] += 1
        else:
            stats["error"] += 1
            errors.append(f"{img_file}: {result}")

    print("\n--- Summary ---")
    print(f"Total processed: {len(all_image_files)}")
    print(f"Converted:       {stats['converted']}")
    print(f"Skipped:         {stats['skipped']}")
    print(f"Errors:          {stats['error']}")
    
    if errors:
        print("\n--- Errors ---")
        for err in errors:
            print(err)
    
    print(f"\nOutput saved to: {output_base}")

if __name__ == "__main__":
    main()
