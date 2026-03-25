from __future__ import annotations

from pathlib import Path

from .models import HermesMcpConfig, HermesProviderConfig, TunnelConfig, VpsConfig


def provider_env_example(provider: HermesProviderConfig, vps: VpsConfig, tunnel: TunnelConfig) -> str:
    return "\n".join(
        [
            "# Hermes provider environment example.",
            "# Copy this to your real Hermes env file and fill in the secrets.",
            f"OPENAI_API_KEY={provider.openai_api_key}",
            f"HERMES_MODEL={provider.model}",
            "# OBSIDIAN_API_KEY intentionally not stored on VPS (Windows-local only).",
            f"VPS_HOST={vps.host}",
            f"VPS_SSH_PORT={vps.ssh_port}",
            f"VPS_USER={vps.user}",
            f"VPS_REMOTE_PORT={tunnel.remote_port}",
            "",
        ]
    )


def mcp_snippet(mcp: HermesMcpConfig) -> str:
    return f'''mcp_servers:
  obsidian:
    url: "{mcp.url}"
    headers:
      Authorization: "Bearer ${{OBSIDIAN_API_KEY}}"
    timeout: 30
    connect_timeout: 10
    tools:
      prompts: false
      resources: false
'''


def windows_env_example(windows_username: str, vps: VpsConfig, tunnel: TunnelConfig, ssh_exe_path: str, log_file_path: str) -> str:
    return "\n".join(
        [
            "# Windows-local reverse SSH and verification values.",
            f"WINDOWS_USERNAME={windows_username}",
            f"OBSIDIAN_LOCAL_PORT={tunnel.local_port}",
            "OBSIDIAN_API_KEY=replace-with-your-obsidian-api-key",
            f"VPS_HOST={vps.host}",
            f"VPS_SSH_PORT={vps.ssh_port}",
            f"VPS_USER={vps.user}",
            f"VPS_REMOTE_PORT={tunnel.remote_port}",
            f"SSH_EXE_PATH={ssh_exe_path}",
            f"SSH_LOG_PATH={log_file_path}",
            "",
        ]
    )


def display_path(path: Path) -> str:
    return str(path)
