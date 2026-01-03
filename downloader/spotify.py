import subprocess
import json
from pathlib import Path

FFMPEG_PATH = r"C:\Users\U1\miniconda3\envs\msc-scrp-1\Library\bin\ffmpeg.exe"

def extract_spotify_metadata(spotify_url: str, output_file: Path) -> list[dict]:
    if output_file.suffix != ".spotdl":
        raise ValueError("spotdl save file must end with .spotdl")

    cmd = [
        "spotdl",
        "save",
        spotify_url,
        "--save-file",
        str(output_file),
        "--overwrite",
        "skip",
        "--ffmpeg",
        FFMPEG_PATH,
    ]

    subprocess.run(cmd, check=True)

    with open(output_file, "r", encoding="utf-8") as f:
        return json.load(f)
