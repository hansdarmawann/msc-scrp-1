from yt_dlp import YoutubeDL
from pathlib import Path

def download_from_search(query: str, output_dir: Path) -> dict:
    """
    Download audio as AAC (CBR) in M4A container
    """

    ydl_opts = {
        "format": "bestaudio/best",
        "default_search": "ytsearch1",
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",   # AAC in MP4 container
                "preferredquality": "256",
            }
        ],
        "postprocessor_args": [
            "-vn",
            "-acodec", "aac",
            "-b:a", "256k",   # CBR
        ],
        "quiet": True,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)

    if "entries" in info:
        info = info["entries"][0]

    # yt-dlp gives us the final filepath
    filepath = info["requested_downloads"][0]["filepath"]
    info["_filepath"] = filepath

    return info
