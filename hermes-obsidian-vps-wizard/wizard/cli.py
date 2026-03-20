from __future__ import annotations

import argparse
import getpass
from pathlib import Path
from typing import Dict, Iterable, Tuple

from .checks import REQUIRED_OUTPUTS, assert_contains, assert_exists, build_verification_plan
from .detect import detect_ssh_exe, repo_root
from .hermes_config import display_path, mcp_snippet, provider_env_example, windows_env_example
from .io_utils import write_many
from .models import HermesMcpConfig, HermesProviderConfig, TunnelConfig, VpsConfig, WindowsLocalConfig, WizardOutputs
from .render import render_template
from .validate import (
    ValidationError,
    validate_hostname_or_ip,
    validate_model,
    validate_port,
    validate_secret,
    validate_ssh_exe,
    validate_username,
    validate_writable_directory,
    warn_if_ports_clash,
)

ROOT = repo_root()
TEMPLATES = ROOT / "templates"
GENERATED_EXAMPLES = ROOT / "generated_examples"


def prompt(label: str, default: str | None = None, secret: bool = False) -> str:
    suffix = f" [{default}]" if default is not None else ""
    if secret:
        response = getpass.getpass(f"{label}{suffix}: ")
    else:
        response = input(f"{label}{suffix}: ").strip()
    return response or (default or "")


def prompt_bool(label: str, default: bool) -> bool:
    rendered_default = "Y/n" if default else "y/N"
    response = input(f"{label} [{rendered_default}]: ").strip().lower()
    if not response:
        return default
    return response in {"y", "yes"}


def write_outputs(output_dir: Path, rendered: Dict[str, str], dry_run: bool = False) -> WizardOutputs:
    files = {output_dir / name: content for name, content in rendered.items()}
    write_many(files, dry_run=dry_run)
    return WizardOutputs(
        output_dir=output_dir,
        files_written=list(files.keys()),
        rendered=rendered,
        dry_run=dry_run,
    )


def common_context(vps: VpsConfig, tunnel: TunnelConfig) -> Dict[str, object]:
    return {
        "VPS_HOST": vps.host,
        "VPS_SSH_PORT": vps.ssh_port,
        "VPS_USER": vps.user,
        "VPS_REMOTE_PORT": tunnel.remote_port,
        "OBSIDIAN_LOCAL_PORT": tunnel.local_port,
        "HERMES_CONFIG_PATH": display_path(vps.hermes_config_path),
        "HERMES_ENV_PATH": display_path(vps.hermes_env_path),
    }


def render_vps_outputs(vps: VpsConfig, provider: HermesProviderConfig, tunnel: TunnelConfig) -> Dict[str, str]:
    context = common_context(vps, tunnel)
    context["HERMES_MODEL"] = provider.model
    rendered = {
        "install_hermes_vps.sh": render_template(TEMPLATES / "install_hermes_vps.sh.tpl", context),
        "hermes_mcp_snippet.yaml": mcp_snippet(HermesMcpConfig(config_path=vps.hermes_config_path, remote_port=tunnel.remote_port)),
        "hermes_provider_env.example": provider_env_example(provider, vps, tunnel),
        "verify_vps_mcp.sh": render_template(TEMPLATES / "verify_vps_mcp.sh.tpl", context),
        "sshd_reverse_forwarding_check.sh": render_template(TEMPLATES / "sshd_reverse_forwarding_check.sh.tpl", context),
    }
    if vps.create_systemd_healthcheck:
        rendered["hermes-obsidian-healthcheck.service"] = render_template(
            TEMPLATES / "systemd" / "hermes-obsidian-healthcheck.service.tpl", context
        )
        rendered["hermes-obsidian-healthcheck.timer"] = render_template(
            TEMPLATES / "systemd" / "hermes-obsidian-healthcheck.timer.tpl", context
        )
    return rendered


def render_windows_outputs(windows: WindowsLocalConfig, vps: VpsConfig, tunnel: TunnelConfig) -> Dict[str, str]:
    ssh_path = windows.ssh_exe_path or detect_ssh_exe() or r"C:\Windows\System32\OpenSSH\ssh.exe"
    context = common_context(vps, tunnel)
    context.update(
        {
            "WINDOWS_USERNAME": windows.windows_username,
            "SSH_EXE_PATH": ssh_path,
            "SSH_LOG_PATH": windows.log_file_path,
            "OBSIDIAN_API_KEY": windows.obsidian_api_key,
        }
    )
    return {
        ".env.example": windows_env_example(windows.windows_username, vps, tunnel, ssh_path, windows.log_file_path),
        "setup_reverse_ssh_windows.ps1": render_template(TEMPLATES / "setup_reverse_ssh_windows.ps1.tpl", context),
        "verify_windows_local.ps1": render_template(TEMPLATES / "verify_windows_local.ps1.tpl", context),
    }


def validate_vps_inputs(vps: VpsConfig, tunnel: TunnelConfig, provider: HermesProviderConfig) -> None:
    validate_hostname_or_ip(vps.host)
    validate_port(vps.ssh_port, "VPS SSH port")
    validate_port(tunnel.remote_port, "VPS remote port")
    validate_username(vps.user, "VPS user")
    validate_model(provider.model)
    validate_writable_directory(ROOT)


def validate_windows_inputs(vps: VpsConfig, tunnel: TunnelConfig, windows: WindowsLocalConfig, require_ssh_exe: bool = True) -> None:
    validate_hostname_or_ip(vps.host)
    validate_port(vps.ssh_port, "VPS SSH port")
    validate_port(tunnel.remote_port, "VPS remote port")
    validate_port(tunnel.local_port, "Obsidian local port")
    validate_username(vps.user, "VPS user")
    validate_username(windows.windows_username, "Windows username")
    validate_secret(windows.obsidian_api_key, "Obsidian API key")
    validate_writable_directory(ROOT)
    if require_ssh_exe and windows.ssh_exe_path:
        validate_ssh_exe(windows.ssh_exe_path)


def print_outputs(outputs: WizardOutputs) -> None:
    heading = "Dry run only. Files that would be written:" if outputs.dry_run else "Wrote files:"
    print(heading)
    for path in outputs.files_written:
        print(f"- {path}")
    for warning in outputs.warnings:
        print(f"Warning: {warning}")


def build_example_configs() -> Tuple[VpsConfig, HermesProviderConfig, TunnelConfig, WindowsLocalConfig]:
    vps = VpsConfig(host="vps.example.net", ssh_port=22, user="hermes")
    provider = HermesProviderConfig(model="gpt-5.4")
    tunnel = TunnelConfig(local_port=27124, remote_port=37124)
    windows = WindowsLocalConfig(
        windows_username="ExampleUser",
        obsidian_local_port=27124,
        obsidian_api_key="example-obsidian-key",
        ssh_exe_path=r"C:\Windows\System32\OpenSSH\ssh.exe",
    )
    return vps, provider, tunnel, windows


def command_vps_setup(_: argparse.Namespace) -> int:
    vps = VpsConfig(
        host=prompt("VPS host"),
        ssh_port=int(prompt("VPS ssh port", "22")),
        user=prompt("VPS user"),
        hermes_config_path=Path(prompt("Hermes config path", "~/.hermes/config.yaml")),
        hermes_env_path=Path(prompt("Hermes env file path", "~/.hermes/.env")),
        create_systemd_healthcheck=prompt_bool("Create a systemd healthcheck timer", True),
    )
    tunnel = TunnelConfig(local_port=27124, remote_port=int(prompt("Remote forwarded port on VPS loopback", "37124")))
    provider = HermesProviderConfig(model=prompt("OpenAI model", "gpt-5.4"), env_file_path=vps.hermes_env_path)
    validate_vps_inputs(vps, tunnel, provider)
    outputs = write_outputs(ROOT, render_vps_outputs(vps, provider, tunnel))
    warning = warn_if_ports_clash(tunnel.local_port, tunnel.remote_port)
    if warning:
        outputs.warnings.append(warning)
    print_outputs(outputs)
    return 0


def command_windows_local_setup(_: argparse.Namespace) -> int:
    default_ssh = detect_ssh_exe() or r"C:\Windows\System32\OpenSSH\ssh.exe"
    windows = WindowsLocalConfig(
        windows_username=prompt("Windows username"),
        obsidian_local_port=int(prompt("Local Obsidian CLI REST port", "27124")),
        obsidian_api_key=prompt("Obsidian API key", secret=True),
        ssh_exe_path=prompt("Path to ssh.exe", default_ssh),
        create_task_scheduler_notes=prompt_bool("Generate Task Scheduler instructions", True),
    )
    vps = VpsConfig(host=prompt("VPS host"), ssh_port=int(prompt("VPS ssh port", "22")), user=prompt("VPS user"))
    tunnel = TunnelConfig(local_port=windows.obsidian_local_port, remote_port=int(prompt("VPS forwarded port", "37124")))
    validate_windows_inputs(vps, tunnel, windows)
    outputs = write_outputs(ROOT, render_windows_outputs(windows, vps, tunnel))
    warning = warn_if_ports_clash(tunnel.local_port, tunnel.remote_port)
    if warning:
        outputs.warnings.append(warning)
    if windows.create_task_scheduler_notes:
        outputs.warnings.append("Task Scheduler persistence instructions are documented in docs/WINDOWS_LOCAL_SETUP.md.")
    print_outputs(outputs)
    return 0


def command_verify(_: argparse.Namespace) -> int:
    errors = assert_exists(ROOT, REQUIRED_OUTPUTS)
    if not errors:
        checks = [
            assert_contains(ROOT / "hermes_provider_env.example", "OPENAI_API_KEY="),
            assert_contains(ROOT / "hermes_provider_env.example", "HERMES_MODEL="),
            assert_contains(ROOT / "hermes_provider_env.example", "OBSIDIAN_API_KEY="),
            assert_contains(ROOT / "hermes_provider_env.example", "HERMES_MODEL=gpt-5.4"),
            assert_contains(ROOT / "hermes_provider_env.example", "VPS_REMOTE_PORT="),
            assert_contains(ROOT / "hermes_mcp_snippet.yaml", 'url: "http://127.0.0.1:'),
            assert_contains(ROOT / "hermes_mcp_snippet.yaml", 'Authorization: "Bearer ${OBSIDIAN_API_KEY}"'),
            assert_contains(ROOT / "setup_reverse_ssh_windows.ps1", "ssh -N -R 127.0.0.1:"),
            assert_contains(ROOT / "setup_reverse_ssh_windows.ps1", ":127.0.0.1:"),
            assert_contains(ROOT / "verify_vps_mcp.sh", "Authorization: Bearer"),
            assert_contains(ROOT / "verify_windows_local.ps1", "/mcp"),
            assert_contains(ROOT / "sshd_reverse_forwarding_check.sh", "AllowTcpForwarding"),
            assert_contains(ROOT / "sshd_reverse_forwarding_check.sh", "GatewayPorts"),
        ]
        errors.extend(item for item in checks if item)
    if errors:
        print("Verification failed:")
        for error in errors:
            print(f"- {error}")
        print("Likely fixes:")
        for fix in build_verification_plan(27124, 37124).likely_fixes:
            print(f"- {fix}")
        return 1

    plan = build_verification_plan(27124, 37124)
    print("Generated files validated successfully.")
    print("Windows commands:")
    for command in plan.windows_commands:
        print(f"- {command}")
    print("VPS commands:")
    for command in plan.vps_commands:
        print(f"- {command}")
    print("Likely fixes for failed checks:")
    for fix in plan.likely_fixes:
        print(f"- {fix}")
    return 0


def command_print_manual_steps(_: argparse.Namespace) -> int:
    steps = [
        "1. On Windows 11, open Obsidian Desktop with the vault you want Hermes to access.",
        "2. Enable the local Obsidian CLI REST or MCP-compatible plugin/service in Obsidian.",
        "3. Extract the plugin API key and store it locally on Windows in a safe location.",
        "4. Confirm the local MCP endpoint works at http://127.0.0.1:27124/mcp with Bearer authentication.",
        "5. On the VPS, run sshd_reverse_forwarding_check.sh and confirm reverse forwarding is allowed.",
        "6. Install Hermes on the VPS and prepare the Hermes provider environment file with OPENAI_API_KEY and HERMES_MODEL.",
        "7. Merge hermes_mcp_snippet.yaml into ~/.hermes/config.yaml so Hermes targets 127.0.0.1 on the VPS.",
        "8. Start setup_reverse_ssh_windows.ps1 to open the private reverse tunnel from Windows to the VPS.",
        "9. Run verify_vps_mcp.sh on the VPS and verify the forwarded /mcp endpoint answers with the Obsidian API key.",
        "10. Start Hermes and run an end-to-end tool call against the Obsidian MCP server.",
    ]
    for step in steps:
        print(step)
    return 0


def command_generate_example(_: argparse.Namespace) -> int:
    vps, provider, tunnel, windows = build_example_configs()
    validate_vps_inputs(vps, tunnel, provider)
    validate_windows_inputs(vps, tunnel, windows, require_ssh_exe=False)
    root_rendered = {}
    root_rendered.update(render_vps_outputs(vps, provider, tunnel))
    root_rendered.update(render_windows_outputs(windows, vps, tunnel))
    write_outputs(ROOT, root_rendered)

    example_rendered = {name: content for name, content in root_rendered.items() if name != ".env.example"}
    write_outputs(GENERATED_EXAMPLES, example_rendered)
    print("Generated checked-in examples under generated_examples/ and current working files at the repo root.")
    return 0


def command_dry_run_all(_: argparse.Namespace) -> int:
    vps, provider, tunnel, windows = build_example_configs()
    windows.obsidian_api_key = "redacted"
    validate_vps_inputs(vps, tunnel, provider)
    validate_windows_inputs(vps, tunnel, windows, require_ssh_exe=False)
    rendered = {}
    rendered.update(render_vps_outputs(vps, provider, tunnel))
    rendered.update(render_windows_outputs(windows, vps, tunnel))
    outputs = write_outputs(ROOT, rendered, dry_run=True)
    print_outputs(outputs)
    print("Secrets were not persisted.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Windows-first Hermes + Obsidian VPS setup artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    commands = {
        "vps-setup": command_vps_setup,
        "windows-local-setup": command_windows_local_setup,
        "verify": command_verify,
        "print-manual-steps": command_print_manual_steps,
        "generate-example": command_generate_example,
        "dry-run-all": command_dry_run_all,
    }
    for name, handler in commands.items():
        sub = subparsers.add_parser(name)
        sub.set_defaults(func=handler)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return args.func(args)
    except ValidationError as exc:
        print(f"Validation error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
