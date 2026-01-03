import re
from pathlib import Path

def sanitize_filename(text: str) -> str:
    """
    Replace spaces with dash, remove unsafe characters.
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9\-_.]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")

def build_track_filename(track_no: int, title: str, ext: str = "m4a") -> str:
    clean_title = sanitize_filename(title)
    return f"{track_no:02d}_{clean_title}.{ext}"

def build_output_path(base: Path, artist: str, album: str) -> Path:
    artist_dir = sanitize_filename(artist)
    album_dir = sanitize_filename(album)

    path = base / artist_dir / album_dir
    path.mkdir(parents=True, exist_ok=True)
    return path
