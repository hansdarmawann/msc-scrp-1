@echo off
echo Cleaning runtime state...

if exist downloads rmdir /s /q downloads
if exist downloads_cache.sqlite del downloads_cache.sqlite
if exist spotify_tracks.spotdl del spotify_tracks.spotdl

echo Done. Repository is clean.
