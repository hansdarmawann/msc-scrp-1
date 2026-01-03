from yt_dlp import YoutubeDL

def extract_playlist(url: str) -> list[dict]:
    """
    Extract playlist metadata only (no download)
    """

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
        "yesplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if "entries" not in info:
        return [info]

    return [e for e in info["entries"] if e]
