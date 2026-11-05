from pathlib import Path
import shutil

def preview_organization(folder: Path):
    plan = []
    for item in folder.iterdir():
        if item.is_file():
            ext = item.suffix.lower().lstrip(".") or "no_extension"
            destination = folder / ext.upper()
            plan.append((item, destination / item.name))
    return plan

def execute_organization(plan):
    moved = skipped = 0
    for source, destination in plan:
        if not source.exists() or destination.exists():
            skipped += 1
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        moved += 1
    return moved, skipped
