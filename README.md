# Jovic's Music Scraper

An **educational music pipeline project** built with Python, focusing on **clean architecture, metadata accuracy, and reproducible workflows** rather than content distribution.

This project demonstrates how to:
- Resolve **accurate music metadata** from Spotify
- Retrieve **best-available audio streams** from public sources
- Normalize filenames and directory structures
- Embed metadata and cover art correctly
- Manage state using a **SQLite cache**
- Build a **deterministic, resume-safe pipeline**

> ⚠️ **For educational purposes only.**  
> This repository does not host or distribute copyrighted content.

---

## ✨ Key Features

- 🎵 **Spotify metadata as the source of truth**
- 🔊 **AAC-LC audio in `.m4a` container (CBR 256 kbps)**
- 🧠 **Main artist normalization** (no multi-artist folder noise)
- 🧾 Proper tagging:
  - Title
  - Artist
  - Album
  - Track number
  - Release year
  - Embedded cover art
- 📁 Clean folder structure:
```

artist/album/01_track-title.m4a

````
- ⚡ Parallel downloads (thread-safe)
- ♻️ SQLite cache with skip / force controls
- 🧪 Dry-run mode for safe testing

---

## 🧱 Project Structure

```text
msc-scrp-1/
│
├── main.py                 # Pipeline entry point
│
├── downloader/             # Metadata & download adapters
│   ├── spotify.py
│   ├── spotify_parallel.py
│   ├── yt_track.py
│   └── metadata.py
│
├── utils/                  # CLI, logging, path utilities
│   ├── cli.py
│   ├── logger.py
│   └── paths.py
│
├── cache/                  # SQLite cache layer
│   └── db.py
│
├── scripts/                # Repo hygiene & maintenance
│   ├── reset_state.bat
│   └── reset_state.sh
│
├── README.md               # Project overview
├── USER_GUIDE.md           # Detailed usage guide
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
├── requirements.txt        # Pip dependencies
└── environment.yml         # Conda environment (export-style)
````

---

## ⚙️ Requirements

* Python **3.11**
* `ffmpeg`
* `spotdl`
* `yt-dlp`

---

## 🚀 Setup

### 1️⃣ Create environment

```bash
conda create -n msc-scrp-1 python=3.11
conda activate msc-scrp-1
```

### 2️⃣ Install dependencies

```bash
pip install spotdl yt-dlp mutagen pillow requests
conda install -c conda-forge ffmpeg
```

---

## ▶️ Usage

### Basic run

```bash
python main.py <spotify_album_or_playlist_url>
```

### Dry run (no download)

```bash
python main.py <url> --dry-run
```

### Force re-download (ignore cache)

```bash
python main.py <url> --force
```

### Disable cache completely

```bash
python main.py <url> --no-cache
```

---

## 📂 Output Example

```text
downloads/
└── fourplay/
    └── fourplay/
        ├── 01_foreplay.m4a
        ├── 02_bali-run.m4a
        ├── 03_moonjogger.m4a
        └── ...
```

---

## 🧠 How It Works (High-Level)

1. **Metadata Resolution**
   Spotify album or playlist metadata is resolved using `spotdl` (metadata-only mode).

2. **Audio Retrieval**
   Audio is fetched from public sources using `yt-dlp` and converted to **AAC-LC (CBR 256 kbps)**.

3. **Normalization**

   * Main artist only
   * Clean filenames (lowercase, dash-separated)
   * Track numbers preserved

4. **Tagging**
   Native MP4 tags are embedded directly into `.m4a` files, including cover art.

5. **Caching**
   A SQLite cache prevents unnecessary re-downloads and enables safe resume.

---

## ⚖️ Legal Notice

This project:

* Does **not** include or distribute copyrighted media
* Demonstrates **software engineering techniques**, not content piracy

Use only with:

* Content you own
* Content licensed for redistribution
* Public domain or Creative Commons material

Users are responsible for complying with applicable copyright laws in their jurisdiction.