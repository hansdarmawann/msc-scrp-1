import argparse

def parse_args():
    p = argparse.ArgumentParser(
        prog="music-downloader",
        description="Educational music downloader (metadata-accurate, cache-aware)"
    )

    p.add_argument(
        "url",
        help="Spotify playlist/track URL"
    )

    p.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)"
    )

    p.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if track exists in cache"
    )

    p.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable cache (do not read/write SQLite cache)"
    )

    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show actions without downloading"
    )

    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of tracks (for testing)"
    )

    return p.parse_args()
