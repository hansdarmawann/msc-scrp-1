from pathlib import Path
import shutil

from utils.cli import parse_args
from utils.logger import setup_logger
from utils.paths import build_output_path, build_track_filename

from downloader.spotify import extract_spotify_metadata
from downloader.spotify_parallel import download_spotify_playlist_parallel
from downloader.tagger import tag_m4a

from cache.db import DownloadCache, NullCache

logger = setup_logger()

# Base paths
OUTPUT_BASE = Path("downloads")
CACHE_DB = Path("downloads_cache.sqlite")
SPOTDL_FILE = Path("spotify_tracks.spotdl")


def main():
    args = parse_args()

    logger.info("Starting downloader...")
    logger.info(f"Workers: {args.workers}")

    # Cache handling
    if args.no_cache:
        cache = NullCache()
        logger.info("Cache: DISABLED")
    else:
        cache = DownloadCache(CACHE_DB)
        logger.info("Cache: ENABLED")

    # --------------------------------------------------
    # 1. Extract Spotify metadata (metadata-only)
    # --------------------------------------------------
    tracks = extract_spotify_metadata(
        args.url,
        SPOTDL_FILE
    )

    if args.limit:
        tracks = tracks[: args.limit]
        logger.info(f"Limit applied: {len(tracks)} track(s)")

    # --------------------------------------------------
    # 2. Parallel download (YouTube → AAC/M4A)
    # --------------------------------------------------
    results = download_spotify_playlist_parallel(
        tracks=tracks,
        output_dir=OUTPUT_BASE,
        cache=cache,
        max_workers=args.workers,
        force=args.force,
        dry_run=args.dry_run,
    )

    # --------------------------------------------------
    # 3. Move, rename, tag, cache
    # --------------------------------------------------
    for status, meta, yt_info in results:
        title = meta["title"]

        if status == "skipped":
            logger.info(f"SKIP: {title}")
            continue

        if status == "dry-run":
            logger.info(f"DRY: {title}")
            continue

        if status != "downloaded":
            logger.warning(f"UNKNOWN STATUS ({status}): {title}")
            continue

        # Source file from yt-dlp (deterministic)
        src_path = Path(yt_info["_filepath"])
        if not src_path.exists():
            logger.warning(f"Downloaded file missing: {title}")
            continue

        # Target directory: artist / album
        target_dir = build_output_path(
            OUTPUT_BASE,
            meta["artist"],
            meta["album"],
        )

        # Clean filename with track number
        filename = build_track_filename(
            meta["track_no"],
            meta["title"],
            "m4a",
        )

        target_path = target_dir / filename

        # Move & rename
        shutil.move(src_path, target_path)

        # Tag M4A (AAC container)
        tag_m4a(target_path, meta)

        # Cache write
        if not args.no_cache:
            cache.add(
                meta["spotify_id"],
                meta,
                str(target_path)
            )

        logger.info(f"OK: {filename}")

    logger.info("Done.")


if __name__ == "__main__":
    main()
