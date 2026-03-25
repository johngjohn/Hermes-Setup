from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .models import VerificationPlan

REQUIRED_OUTPUTS = (
    ".env.example",
    "hermes_mcp_snippet.yaml",
    "hermes_provider_env.example",
    "install_hermes_vps.sh",
    "setup_reverse_ssh_windows.ps1",
    "sshd_reverse_forwarding_check.sh",
    "verify_vps_mcp.sh",
    "verify_windows_local.ps1",
)


def assert_exists(root: Path, names: Iterable[str]) -> List[str]:
    errors: List[str] = []
    for name in names:
        if not (root / name).exists():
            errors.append(f"Missing file: {root / name}")
    return errors


def assert_contains(path: Path, needle: str) -> str | None:
    content = path.read_text(encoding="utf-8")
    if needle not in content:
        return f"Expected text not found in {path}: {needle}"
    return None


def build_verification_plan(local_port: int, remote_port: int) -> VerificationPlan:
    return VerificationPlan(
        windows_commands=[
            f"powershell -ExecutionPolicy Bypass -Command \"$env:OBSIDIAN_API_KEY='<OBSIDIAN_API_KEY>'; .\\verify_windows_local.ps1 -LocalPort {local_port}\"",
            ".\\setup_reverse_ssh_windows.ps1",
        ],
        vps_commands=[
            "bash ./sshd_reverse_forwarding_check.sh",
            f"bash ./verify_vps_mcp.sh {remote_port}",
        ],
        likely_fixes=[
            "Obsidian closed or plugin disabled on Windows.",
            "Wrong local or remote port configured in the tunnel or MCP snippet.",
            "Obsidian API key mismatch causing 401/403 responses.",
            "VPS sshd policy blocks reverse forwarding via AllowTcpForwarding or Match rules.",
            "Hermes provider env not loaded or MCP snippet not merged into the live Hermes config.",
        ],
    )
