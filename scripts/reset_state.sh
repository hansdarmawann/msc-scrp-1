#!/usr/bin/env bash
echo "Cleaning runtime state..."

rm -rf downloads
rm -f downloads_cache.sqlite spotify_tracks.spotdl

echo "Done. Repository is clean."
