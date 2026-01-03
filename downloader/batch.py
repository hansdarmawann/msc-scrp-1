from pathlib import Path
from yt_dlp import YoutubeDL

def download_playlist(url: str, output_dir: Path) -> list[dict]:
    """
    Download playlist or batch URLs.
    Returns list of track info dicts.
    """

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(playlist_index)s - %(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }],
        "quiet": True,
        "no_warnings": True,
        "yesplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    # Normalize to list
    if "entries" in info:
        return [e for e in info["entries"] if e]
    else:
        return [info]
