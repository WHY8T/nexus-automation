from pathlib import Path
from collections import defaultdict
import hashlib

def sha256_file(path: Path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

def find_duplicates(folder: Path):
    by_hash = defaultdict(list)
    for path in folder.rglob("*"):
        if path.is_file():
            try:
                by_hash[sha256_file(path)].append(path)
            except (OSError, PermissionError):
                continue
    return [paths for paths in by_hash.values() if len(paths) > 1]
