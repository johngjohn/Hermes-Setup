from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

ALLOWED_DEFAULT_MODELS = ("gpt-5.4", "gpt-5.4-mini")
ALLOWED_ROUTING_MODELS = ("gpt-5.4", "gpt-5.4-mini", "gpt-5.3-codex")
MODEL_ROUTING_MODES = ("auto", "fixed")


@dataclass
class TunnelConfig:
    local_port: int = 27124
    remote_port: int = 37124


@dataclass
class HermesProviderConfig:
    openai_api_key: str = ""
    model: str = "gpt-5.4"
    env_file_path: Path = Path("~/.hermes/.env")
    obsidian_api_key: str = ""
    routing_mode: str = "auto"
    coding_model: str = "gpt-5.3-codex"
    reasoning_model: str = "gpt-5.4"
    fast_model: str = "gpt-5.4-mini"


@dataclass
class HermesMcpConfig:
    config_path: Path = Path("~/.hermes/config.yaml")
    remote_port: int = 37124

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.remote_port}/mcp"


@dataclass
class VpsConfig:
    host: str
    ssh_port: int = 22
    user: str = "hermes"
    hermes_config_path: Path = Path("~/.hermes/config.yaml")
    hermes_env_path: Path = Path("~/.hermes/.env")
    create_systemd_healthcheck: bool = True


@dataclass
class WindowsLocalConfig:
    windows_username: str
    obsidian_local_port: int = 27124
    obsidian_api_key: str = ""
    ssh_exe_path: Optional[str] = None
    create_task_scheduler_notes: bool = True
    log_file_path: str = r"%USERPROFILE%\hermes-obsidian-reverse-ssh.log"


@dataclass
class WizardOutputs:
    output_dir: Path
    files_written: List[Path] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    rendered: Dict[str, str] = field(default_factory=dict)
    dry_run: bool = False


@dataclass
class VerificationPlan:
    windows_commands: List[str] = field(default_factory=list)
    vps_commands: List[str] = field(default_factory=list)
    likely_fixes: List[str] = field(default_factory=list)
