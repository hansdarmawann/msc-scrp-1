from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from yt_dlp import YoutubeDL
import threading

lock = threading.Lock()

def download_single_track(track_info: dict, output_dir: Path) -> dict:
    """
    Thread-safe single track downloader
    """

    video_url = track_info.get("webpage_url")
    if not video_url:
        raise ValueError("Missing webpage_url")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }],
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)

    return info


def parallel_download(
    tracks: list[dict],
    output_dir: Path,
    max_workers: int = 4
) -> list[dict]:

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_single_track, track, output_dir): track
            for track in tracks
        }

        for future in as_completed(futures):
            try:
                info = future.result()
                results.append(info)
            except Exception as e:
                print(f"[ERROR] {e}")

    return results
