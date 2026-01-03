# User Guide — Jovic's Music Scraper

This document explains how to use **Jovic's Music Scraper**, an educational Python project
that demonstrates a **metadata-driven audio processing pipeline** with a focus on
clean architecture, reproducibility, and deterministic behavior.

> ⚠️ **Educational purposes only.**  
> Use this project only with content you own or are legally allowed to access.

---

## 1. What This Project Does

`Jovic's Music Scraper` is designed to showcase **engineering concepts**, not content distribution.

Core ideas demonstrated:
- Using **Spotify metadata as the source of truth**
- Separating metadata resolution from audio retrieval
- Building a **deterministic pipeline** (no guessing, no globbing)
- Managing state explicitly with a **SQLite cache**
- Producing clean, well-tagged audio files

---

## 2. High-Level Pipeline

1. **Metadata Resolution**  
   Spotify album or playlist metadata is resolved using `spotdl` in metadata-only mode.

2. **Audio Retrieval**  
   Audio is fetched from public sources using `yt-dlp`.

3. **Audio Processing**  
   - Codec: AAC-LC  
   - Container: `.m4a`  
   - Bitrate: Constant 256 kbps (CBR)

4. **Normalization**  
   - Main artist only  
   - Clean filenames (lowercase, dash-separated)  
   - Track numbers preserved

5. **Tagging**  
   Native MP4 tags are embedded:
   - Title
   - Artist
   - Album
   - Track number
   - Release year
   - Cover art

6. **Caching**  
   A SQLite cache prevents unnecessary re-processing and enables safe resume.

---

## 3. Prerequisites

- Python **3.11**
- Conda or Mamba
- `ffmpeg` available in the active environment

Recommended setup:

```bash
conda env create -f environment.yml
conda activate Jovic's Music Scraper
````

---

## 4. Basic Usage

### Download an album or playlist

```bash
python main.py <spotify_album_or_playlist_url>
```

Example:

```bash
python main.py https://open.spotify.com/album/XXXXXXXX
```

---

## 5. Common CLI Flags

### Dry run (no download)

```bash
python main.py <url> --dry-run
```

* Resolves metadata
* Shows which tracks would be processed
* Does **not** download audio

---

### Force re-download

```bash
python main.py <url> --force
```

* Ignores cache entries
* Downloads and processes all tracks again
* Useful when changing format, bitrate, or tagging logic

---

### Disable cache

```bash
python main.py <url> --no-cache
```

* Does not read from or write to the cache
* Useful for experiments and one-off runs

---

### Limit number of tracks (testing)

```bash
python main.py <url> --limit 3
```

* Processes only the first N tracks
* Useful for quick validation

---

## 6. Output Structure

Files are organized deterministically:

```text
downloads/
└── artist/
    └── album/
        ├── 01_track-title.m4a
        ├── 02_track-title.m4a
        └── ...
```

Rules:

* **Artist**: main artist only
* **Album**: normalized folder name
* **Filename**:

  * lowercase
  * dash-separated
  * prefixed with zero-padded track number

---

## 7. Cache Behavior

The SQLite cache stores processed Spotify track IDs.

* If a track ID exists in cache → the track is **skipped**
* Cache state is independent of the filesystem

### Reset cache and runtime state

Use the provided scripts:

```bash
scripts/reset_state.bat    # Windows
./scripts/reset_state.sh   # macOS / Linux
```

---

## 8. Troubleshooting

### All tracks are skipped

* The cache still contains previous entries.
* Use `--force` or delete `downloads_cache.sqlite`.

### FFmpeg not found

* Ensure `ffmpeg` is installed in the active conda environment.

### Files are not created

* Run with `--dry-run` first to validate metadata resolution.
* Check network access for external tools.

---

## 9. What This Project Is (and Is Not)

### ✔ This project is:

* An educational example of pipeline design
* A demonstration of metadata normalization and audio processing
* A reproducible and maintainable workflow

### ✖ This project is NOT:

* A media hosting service
* A DRM circumvention tool
* A recommendation to violate copyright laws

---

## 10. License

This project is released under the **MIT License**.
See the `LICENSE` file for details.