from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Optional


def detect_ssh_exe() -> Optional[str]:
    candidates = [
        os.environ.get("SSH_EXE_PATH"),
        r"C:\Windows\System32\OpenSSH\ssh.exe",
        r"C:\Program Files\Git\usr\bin\ssh.exe",
        shutil.which("ssh"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]
