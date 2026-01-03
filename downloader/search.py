from yt_dlp import YoutubeDL

def search_youtube(query: str) -> str:
    """
    Search YouTube and return best matching video URL.
    """

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "default_search": "ytsearch1",
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)

    if "entries" in info and info["entries"]:
        return info["entries"][0]["webpage_url"]

    raise ValueError("No YouTube match found")
