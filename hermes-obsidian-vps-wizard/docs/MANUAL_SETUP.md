# Manual Setup

This document prints the exact ordered manual process that the wizard automates.

## Ordered manual steps

1. On Windows 11, open Obsidian Desktop with the vault Hermes should use.
2. Enable the Obsidian CLI REST or MCP-compatible plugin/service inside Obsidian.
3. Extract the plugin API key and store it locally on Windows.
4. Confirm the plugin is listening on `127.0.0.1:27124` or your chosen local port.
5. Run `verify_windows_local.ps1` with the Obsidian API key and confirm the local `/mcp` endpoint answers.
6. On the VPS, confirm the OpenSSH server is installed and running.
7. Run `sshd_reverse_forwarding_check.sh` and review `AllowTcpForwarding`, `GatewayPorts`, and any `Match` rules.
8. Install Hermes on the VPS and create or update the provider env file containing the OpenAI API key.
9. Merge `hermes_mcp_snippet.yaml` into `~/.hermes/config.yaml` so Hermes points at `http://127.0.0.1:<remote-port>/mcp`.
10. Start `setup_reverse_ssh_windows.ps1` so Windows opens the reverse SSH tunnel to the VPS.
11. Run `verify_vps_mcp.sh` on the VPS and confirm the forwarded endpoint responds.
12. Start Hermes and perform an end-to-end Obsidian MCP test.
