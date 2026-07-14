# Image Converter

*by fancy tools: https://webfancy.pl*

*[Wersja polska](README.md)*

A script for bulk image conversion (defaults to WebP, optionally to another format) that preserves the directory structure and supports optional resizing.

## macOS App

The [MacOS App](MacOS App/) directory contains a native desktop app with the same conversion engine: drag & drop folders/files, WebP / JPEG / PNG / HEIC / TIFF / BMP / GIF output, a quality slider, dimension limits, live progress, and a summary with saved disk space. Conversion runs in parallel on all CPU cores — no Python required.

### Ready-to-use build

Latest release: **v0.1.1** — [download ImageConverter.dmg](<MacOS App/Releases/v0.1.1/ImageConverter.dmg>) — see [CHANGELOG.en.md](CHANGELOG.en.md)

## Installation and usage of the Python version

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the environment:
   - macOS / Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Basic usage (converts everything in `my_photos` and saves the output to `my_photos_webp`):
```bash
python convert_to_webp.py path/to/images
```

### Options:

- `--output`, `-o`: Path to the output directory (defaults to `[input]_[format]`).
- `--format`, `-f`: Output format/extension: `webp`, `jpg`, `jpeg`, `png`, `bmp`, `tiff`, `gif` (default `webp`).
- `--max-landscape-width`: Maximum width for landscape images (default 1920).
- `--max-portrait-height`: Maximum height for portrait images (default 1080).
- `--quality`, `-q`: Quality 0-100, applies to `webp` and `jpg`/`jpeg` formats (default 80).
- `--overwrite`: If present, overwrites existing output files.

Example with custom limits:
```bash
python convert_to_webp.py ./input_images -o ./web_ready --max-landscape-width 1280 --max-portrait-height 720 -q 75
```

Example converting to JPG:
```bash
python convert_to_webp.py ./input_images --format jpg -q 85
```

## License

Free to use and redistribute without modification — see [LICENSE.en.md](LICENSE.en.md).
