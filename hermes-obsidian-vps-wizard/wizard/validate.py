from __future__ import annotations

import ipaddress
import os
import re
from pathlib import Path
from typing import Optional

from .models import ALLOWED_MODELS

SAFE_USERNAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
HOSTNAME_RE = re.compile(r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$")


class ValidationError(ValueError):
    pass


def validate_port(value: int, label: str) -> None:
    if not 1 <= int(value) <= 65535:
        raise ValidationError(f"{label} must be between 1 and 65535.")


def validate_username(value: str, label: str) -> None:
    if not value or not SAFE_USERNAME_RE.fullmatch(value):
        raise ValidationError(f"{label} must be shell-safe: letters, numbers, dot, underscore, and dash only.")


def validate_hostname_or_ip(value: str) -> None:
    if not value.strip():
        raise ValidationError("VPS host must be non-empty.")
    try:
        ipaddress.ip_address(value)
        return
    except ValueError:
        pass
    if not HOSTNAME_RE.fullmatch(value):
        raise ValidationError(f"Invalid hostname or IP address: {value}")


def validate_model(value: str) -> None:
    if value not in ALLOWED_MODELS:
        raise ValidationError(f"Model must be one of: {', '.join(ALLOWED_MODELS)}")


def validate_secret(value: str, label: str) -> None:
    if not value.strip():
        raise ValidationError(f"{label} must be non-empty.")


def validate_writable_directory(path: Path) -> None:
    target = path.expanduser()
    parent = target if target.is_dir() else target.parent
    while not parent.exists() and parent != parent.parent:
        parent = parent.parent
    if not os.access(parent, os.W_OK):
        raise ValidationError(f"Directory is not writable: {parent}")


def validate_ssh_exe(path_value: Optional[str]) -> Optional[str]:
    if not path_value:
        return None
    if not Path(path_value).exists():
        raise ValidationError(
            f"ssh.exe was not found at {path_value}. Install Windows OpenSSH Client or set the correct path."
        )
    return path_value


def warn_if_ports_clash(local_port: int, remote_port: int) -> Optional[str]:
    if local_port == remote_port:
        return "Local and remote tunnel ports match. That works, but it can make troubleshooting harder."
    return None
