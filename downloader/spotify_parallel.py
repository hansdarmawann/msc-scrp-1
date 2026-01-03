from concurrent.futures import ThreadPoolExecutor, as_completed
from downloader.yt_track import download_from_search
from downloader.metadata import normalize_spotify_track

def download_spotify_playlist_parallel(
    tracks: list[dict],
    output_dir,
    cache,
    max_workers=4,
    force=False,
    dry_run=False,
):
    results = []

    def worker(idx_track):
        idx, track = idx_track
        meta = normalize_spotify_track(track, idx + 1)

        if not force and cache.exists(meta["spotify_id"]):
            return ("skipped", meta, None)

        if dry_run:
            return ("dry-run", meta, None)

        yt_info = download_from_search(meta["search_query"], output_dir)
        return ("downloaded", meta, yt_info)

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [
            ex.submit(worker, pair)
            for pair in enumerate(tracks)
        ]

        for f in as_completed(futures):
            results.append(f.result())

    return results
