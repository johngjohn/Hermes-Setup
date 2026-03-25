from __future__ import annotations

from pathlib import Path

from .models import HermesMcpConfig, HermesProviderConfig, TunnelConfig, VpsConfig


def provider_env_example(provider: HermesProviderConfig, vps: VpsConfig, tunnel: TunnelConfig) -> str:
    return "\n".join(
        [
            "# Hermes provider environment example.",
            "# Copy this to your real Hermes env file and fill in the secrets.",
            "OPENAI_API_KEY=<REPLACE_ME>",
            f"HERMES_MODEL={provider.model}",
            f"HERMES_MODEL_MODE={provider.routing_mode}",
            f"HERMES_MODEL_CODING={provider.coding_model}",
            f"HERMES_MODEL_REASONING={provider.reasoning_model}",
            f"HERMES_MODEL_FAST={provider.fast_model}",
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


def model_routing_yaml(provider: HermesProviderConfig) -> str:
    return f'''# Operator model routing policy for Hermes + Obsidian tasks.
# Mode: auto = choose by task class, fixed = always use fallback/default model.
mode: {provider.routing_mode}
default_model: {provider.model}
models:
  coding: {provider.coding_model}
  reasoning: {provider.reasoning_model}
  fast: {provider.fast_model}
routing_rules:
  - class: coding
    when_any:
      - code
      - script
      - javascript
      - html
      - css
      - python
      - debug
      - refactor
  - class: reasoning
    when_any:
      - design
      - architecture
      - policy
      - plan
      - summary
  - class: fast
    when_any:
      - quick
      - simple
      - short
      - check
'''


def windows_env_example(windows_username: str, vps: VpsConfig, tunnel: TunnelConfig, ssh_exe_path: str, log_file_path: str) -> str:
    return "\n".join(
        [
            "# Windows-local reverse SSH and verification values.",
            f"WINDOWS_USERNAME={windows_username}",
            f"OBSIDIAN_LOCAL_PORT={tunnel.local_port}",
            "OBSIDIAN_API_KEY=<REPLACE_ME>",
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
