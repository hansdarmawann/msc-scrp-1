import sqlite3
from pathlib import Path
import threading
from datetime import datetime

_DB_LOCK = threading.Lock()

class NullCache:
    def exists(self, *_):
        return False

    def add(self, *_):
        pass

class DownloadCache:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    spotify_id TEXT PRIMARY KEY,
                    title TEXT,
                    artist TEXT,
                    album TEXT,
                    year TEXT,
                    duration INTEGER,
                    file_path TEXT,
                    downloaded_at TEXT
                )
            """)
            conn.commit()

    def exists(self, spotify_id: str) -> bool:
        with _DB_LOCK, self._connect() as conn:
            cur = conn.execute(
                "SELECT 1 FROM downloads WHERE spotify_id = ?",
                (spotify_id,)
            )
            return cur.fetchone() is not None

    def add(self, spotify_id: str, meta: dict, file_path: str):
        with _DB_LOCK, self._connect() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO downloads (
                    spotify_id,
                    title,
                    artist,
                    album,
                    year,
                    duration,
                    file_path,
                    downloaded_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                spotify_id,
                meta["title"],
                meta["artist"],
                meta["album"],
                meta["year"],
                meta["duration"],
                file_path,
                datetime.utcnow().isoformat()
            ))
            conn.commit()
