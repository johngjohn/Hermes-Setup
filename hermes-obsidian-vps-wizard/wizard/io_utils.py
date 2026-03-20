from __future__ import annotations

from pathlib import Path
from typing import Dict


def ensure_directory(path: Path, dry_run: bool = False) -> None:
    if dry_run:
        return
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str, dry_run: bool = False) -> None:
    ensure_directory(path.parent, dry_run=dry_run)
    if dry_run:
        return
    path.write_text(content, encoding="utf-8")


def write_many(files: Dict[Path, str], dry_run: bool = False) -> None:
    for path, content in files.items():
        write_text(path, content, dry_run=dry_run)
