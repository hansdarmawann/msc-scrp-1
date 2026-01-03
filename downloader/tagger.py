from mutagen.mp4 import MP4, MP4Cover
import requests

def tag_m4a(file_path, meta: dict):
    audio = MP4(file_path)

    audio["\xa9nam"] = meta["title"]            # Title
    audio["\xa9ART"] = meta["artist"]           # Artist
    audio["\xa9alb"] = meta["album"]            # Album
    audio["trkn"] = [(meta["track_no"], 0)]     # Track number

    if meta.get("year"):
        audio["\xa9day"] = meta["year"]

    if meta.get("cover_url"):
        img = requests.get(meta["cover_url"], timeout=10).content
        audio["covr"] = [MP4Cover(img, imageformat=MP4Cover.FORMAT_JPEG)]

    audio.save()
