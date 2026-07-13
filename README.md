# Image Converter

*by fancy tools: https://webfancy.pl*

*[English version](README.en.md)*

Skrypt do masowej konwersji obrazów (domyślnie na WebP, opcjonalnie na inny format) z zachowaniem struktury katalogów i opcjonalnym skalowaniem.

## Instalacja

1. Stwórz wirtualne środowisko:
   ```bash
   python3 -m venv venv
   ```

2. Aktywuj środowisko:
   - macOS / Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```

## Użycie

Podstawowe użycie (konwertuje wszystko w `moje_zdjecia` i zapisuje w `moje_zdjecia_webp`):
```bash
python convert_to_webp.py path/to/images
```

### Opcje:

- `--output`, `-o`: Ścieżka do katalogu wyjściowego (domyślnie `[input]_[format]`).
- `--format`, `-f`: Format/rozszerzenie wyjściowe: `webp`, `jpg`, `jpeg`, `png`, `bmp`, `tiff`, `gif` (domyślnie `webp`).
- `--max-landscape-width`: Maksymalna szerokość dla zdjęć poziomych (domyślnie 1920).
- `--max-portrait-height`: Maksymalna wysokość dla zdjęć pionowych (domyślnie 1080).
- `--quality`, `-q`: Jakość 0-100, dotyczy formatów `webp` i `jpg`/`jpeg` (domyślnie 80).
- `--overwrite`: Jeśli flaga jest obecna, nadpisuje istniejące pliki wyjściowe.

Przykład z własnymi limitami:
```bash
python convert_to_webp.py ./input_images -o ./web_ready --max-landscape-width 1280 --max-portrait-height 720 -q 75
```

Przykład konwersji do JPG:
```bash
python convert_to_webp.py ./input_images --format jpg -q 85
```
