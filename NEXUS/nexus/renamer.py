from pathlib import Path

def preview_rename(folder: Path, prefix: str, start: int = 1):
    files = sorted((p for p in folder.iterdir() if p.is_file()), key=lambda p: p.name.lower())
    pairs = []
    for index, source in enumerate(files, start):
        destination = folder / f"{prefix}_{index:03d}{source.suffix.lower()}"
        if destination.exists() and destination != source:
            return [], f"Cannot rename safely: {destination.name} already exists."
        pairs.append((source, destination))
    return pairs, None

def execute_rename(pairs):
    # Stage through temporary names to avoid collisions between source and destination names.
    staged = []
    try:
        for index, (source, destination) in enumerate(pairs):
            temp = source.with_name(f".nexus_tmp_{index}_{source.name}")
            if temp.exists():
                raise FileExistsError(temp)
            source.rename(temp)
            staged.append((temp, destination))
        for temp, destination in staged:
            if destination.exists():
                raise FileExistsError(destination)
        for temp, destination in staged:
            temp.rename(destination)
        return len(staged), None
    except OSError as exc:
        # Restore any files that are still staged where possible.
        for temp, destination in staged:
            if temp.exists():
                original = next((src for src, dst in pairs if dst == destination), None)
                if original and not original.exists():
                    temp.rename(original)
        return 0, str(exc)
