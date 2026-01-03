def normalize_spotify_track(track: dict, index: int) -> dict:
    """
    Normalize spotdl v5+ metadata
    - Use MAIN artist only
    """

    artists = track.get("artists")

    # Ambil artis utama saja
    if isinstance(artists, list) and artists:
        main_artist = artists[0]
    elif isinstance(artists, str):
        main_artist = artists.split(",")[0]
    else:
        main_artist = "unknown-artist"

    return {
        "spotify_id": track.get("song_id"),
        "track_no": index,
        "title": track.get("name"),
        "artist": main_artist,
        "album": track.get("album_name"),
        "year": str(track.get("album_year") or ""),
        "duration": track.get("duration"),
        "cover_url": track.get("cover_url"),
        "search_query": f'{track.get("name")} {main_artist}',
    }
